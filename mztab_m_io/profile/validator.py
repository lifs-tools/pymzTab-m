import json
import logging
import pathlib
import time
from importlib import resources
from pathlib import Path
from typing import Annotated, Literal, Union

from jsonprofile.profile import JsonProfile, ValidationRuntimeConfiguration
from jsonprofile.validator import CvTermSearch, JsonValidationResult, JsonValidator
from pydantic import Field, ValidationError

import mztab_m_io
from mztab_m_io.model.mztabm import MzTabM
from mztab_m_io.model.validation import (
    Category,
    MessageType,
    MzTabMessage,
    ValidationContext,
)
from mztab_m_io.profile.default_profile import DEFAULT_PROFILE

logger = logging.getLogger(__name__)

_root_path = Path(resources.files(mztab_m_io.__name__))
MZTABM_JSONSCHEMA_PATH = _root_path / Path("resources/mztabm-2.1.0-M.schema.json")

_profiles_path = _root_path / Path("resources/profiles")
DEFAULT_PROFILE_PATH = _profiles_path / Path("mztabm-default-profile-2.1.0-M.json")


class MzTabMProfileValidator(JsonValidator):
    def __init__(
        self,
        profile: Annotated[
            None | str | Path | dict | JsonProfile,
            Field(
                description="Json profile file path or dictionary."
                " If it is not defined, default profile will be used."
            ),
        ],
        referenced_profiles: Annotated[
            dict[
                str,
                Union[str | Path, dict | JsonProfile],
            ],
            Field(
                description="Additional profile ids referenced (`extends`, etc.) "
                "in the profile and their sources. "
                "Default profile will be automatically injected."
            ),
        ] = None,
        default_cv_term_search: Annotated[
            CvTermSearch,
            Field(description="Default cv term search implementation "),
        ] = None,
    ):
        if not referenced_profiles:
            referenced_profiles = {DEFAULT_PROFILE.id: str(DEFAULT_PROFILE_PATH)}
        elif DEFAULT_PROFILE.id not in referenced_profiles:
            referenced_profiles[DEFAULT_PROFILE.id] = str(DEFAULT_PROFILE_PATH)
        if not profile:
            profile = DEFAULT_PROFILE
        super().__init__(
            json_schema=MZTABM_JSONSCHEMA_PATH,
            profile=profile,
            referenced_profiles=referenced_profiles,
            default_cv_term_search=default_cv_term_search,
        )


class MzTabMLoader:
    def __init__(
        self,
        profile: Annotated[
            None | str | Path | dict | JsonProfile,
            Field(
                description="Json profile file path or dictionary."
                " If it is not defined, default profile will be used."
            ),
        ],
        referenced_profiles: Annotated[
            dict[
                str,
                Union[str | Path, dict | JsonProfile],
            ],
            Field(
                description="Additional profile ids referenced (`extends`, etc.) "
                "in the profile and their sources. "
                "Default profile will be automatically injected."
            ),
        ] = None,
        default_cv_term_search: Annotated[
            CvTermSearch,
            Field(description="Default cv term search implementation "),
        ] = None,
    ):
        self.profile_validator = MzTabMProfileValidator(
            profile=profile,
            referenced_profiles=referenced_profiles,
            default_cv_term_search=default_cv_term_search,
        )

    def read(
        self,
        file_path: str,
        format: Literal["tsv", "json", "yaml"] = "tsv",
        auto_complete_ids: bool = False,
        runtime_config: None | ValidationRuntimeConfiguration = None,
    ) -> mztab_m_io.MzTabMLoadResult:
        if not file_path:
            raise ValueError("Invalid file path")
        if not format:
            raise ValueError("Invalid file format.")

        input_path = pathlib.Path(file_path)
        if not input_path.exists():
            raise ValueError("Input file does not exist.")
        result = None
        if format == "tsv":
            result = mztab_m_io.MzTabMLoadResult(
                success=False,
                messages=[],
                source_format="tsv",
                auto_complete_ids=auto_complete_ids,
            )
            try:
                mztabm, context = MzTabM.from_tsv_file(
                    input_path,
                    context=ValidationContext(
                        source_format="tsv",
                        auto_complete_ids=auto_complete_ids,
                    ),
                )
                result.mztabm = mztabm
                if mztabm:
                    result.success = True
                result.messages.extend(context.messages)
            except ValidationError as ex:
                result.messages.extend(
                    [
                        MzTabMessage(
                            category=Category.FORMAT,
                            message_type=MessageType.ERROR,
                            message=repr(x),
                            source="",
                        )
                        for x in ex.errors()
                    ]
                )
        elif format == "json" or format == "yaml":
            context = ValidationContext(
                source_format=format,
                auto_complete_ids=auto_complete_ids,
            )
            if format == "json":
                mztabm, context = MzTabM.from_json_file(input_path, context=context)
            else:
                mztabm, context = MzTabM.from_yaml_file(input_path, context=context)
            success = False
            errors = [
                x for x in context.messages if x.message_type == MessageType.ERROR
            ]
            if not errors and mztabm:
                success = True

            result = mztab_m_io.MzTabMLoadResult(
                success=success, mztabm=mztabm, messages=context.messages
            )
        else:
            raise ValueError(f"invalid format type: {format}")
        if result and result.mztabm:
            validation_start = time.perf_counter()
            self._validate(
                source=result.mztabm,
                messages=result.messages,
                runtime_config=runtime_config,
            )
            validation_end = time.perf_counter()
            logger.info(
                "MzTabM validation execution time: %.6f seconds",
                (validation_end - validation_start),
            )
        else:
            result.messages.append(
                MzTabMessage(
                    category=Category.FORMAT,
                    message_type=MessageType.ERROR,
                    message="MzTabM file content is not valid",
                )
            )
        return result

    def _validate(
        self,
        source: dict | MzTabM | pathlib.Path | bytes | str,
        messages: None | list[MzTabMessage] = None,
        runtime_config: None | ValidationRuntimeConfiguration = None,
    ) -> list[MzTabMessage]:
        if messages is None:
            messages = []
        mztabm_input = None
        if isinstance(source, MzTabM):
            mztabm_input = source.model_dump(by_alias=True)
        elif isinstance(source, dict):
            mztabm_input = source
        elif isinstance(source, pathlib.Path):
            mztabm_input = json.loads(source.read_text())
        elif isinstance(source, str):
            mztabm_input = json.loads(source)
        else:
            raise ValueError("source is not valid")
        if not runtime_config:
            runtime_config = ValidationRuntimeConfiguration()

        validation_result: JsonValidationResult = self.profile_validator.validate_dict(
            input_json=mztabm_input, runtime_config=runtime_config
        )
        for message_type, message_dict in [
            (MessageType.ERROR, validation_result.errors),
            (MessageType.WARNING, validation_result.recommendations),
            (MessageType.INFO, validation_result.optionals),
        ]:
            for _, items in message_dict.items() or {}:
                for item in items:
                    messages.append(
                        MzTabMessage(
                            code=item.code or "",
                            category=Category.PROFILE,
                            message_type=message_type,
                            message=item.message,
                            source=item.source,
                        )
                    )
        return messages
