import json
import logging
import traceback
from pathlib import Path

from mztab_m_io import MzTabMLoadResult, read
from mztab_m_io.model.validation import Category, MzTabMessage
from mztab_m_io.profile.constraints import ValidationRuntimeConfiguration
from mztab_m_io.profile.default_profile import DEFAULT_PROFILE
from mztab_m_io.profile.metabolights_profile import METABOLIGHTS_PROFILE
from mztab_m_io.profile.model import MzTabMProfile
from mztab_m_io.profile.profile_validator import validate_profile_file
from mztab_m_io.validator.mztabm_validator import MzTabMValidator
from scripts.utils import setup_basic_logging_config

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    setup_basic_logging_config()
    profiles = Path("mztab_m_io/resources/profiles")
    profile_schema_json = MzTabMProfile.model_json_schema(
        by_alias=True, mode="serialization"
    )
    profile_schema = profiles / Path("mztabm-profile-2.1.0-M.schema.json")
    with profile_schema.open("w") as f:
        json.dump(profile_schema_json, f, indent=4)

    default_profile_path = profiles / Path("mztabm-default-profile-2.1.0-M.json")
    with default_profile_path.open("w") as f:
        json.dump(DEFAULT_PROFILE.model_dump(exclude_none=True), f, indent=4)

    mtbls_profile_path = profiles / Path("mztabm-metabolights-profile-2.1.0-M.json")
    valid, messages = validate_profile_file(mtbls_profile_path)
    valid_message = "Valid" if valid else "Invalid"
    logger.info("%s profile file: %s", valid_message, mtbls_profile_path)

    for message in messages:
        type_ = message.message_type.name
        logger.info(
            "%s\t%s (%s): %s",
            type_,
            message.code or "-",
            message.source,
            message.message,
        )
    with mtbls_profile_path.open("w") as f:
        json.dump(METABOLIGHTS_PROFILE.model_dump(exclude_none=True), f, indent=4)

    files = list(Path("tests/data/mztabm").glob("*.mz?ab"))
    profile_json = json.loads(mtbls_profile_path.read_text())
    validator = MzTabMValidator(profile=profile_json)
    max_same_error_code = 10
    runtime_config = ValidationRuntimeConfiguration(
        max_messages_for_each_requirement=10, skip_decimal_validations=True
    )
    for idx, file_path in enumerate(files, start=1):
        try:
            logger.info("%s", 120 * "-")
            logger.info("(%s / %s) %s will be validated.", idx, len(files), file_path)
            logger.info("%s", 120 * "-")

            result: MzTabMLoadResult = read(
                str(file_path), validator=validator, runtime_config=runtime_config
            )
            result_file_path = Path("./output") / Path(f"{file_path.name}.result.json")
            json_file_path = Path("./output") / Path(f"{file_path.name}.json")
            results_json = result.model_dump(by_alias=True)
            with result_file_path.open("w") as f:
                json.dump({"messages": results_json.get("messages", [])}, f, indent=2)
            with json_file_path.open("w") as f:
                json.dump({"messages": results_json.get("mztabm", {})}, f, indent=2)

            profile_messages = [
                x for x in result.messages if x.category == Category.PROFILE
            ]
            messages_counts = {}
            latest_code = None
            messages_based_on_codes: dict[str, list[MzTabMessage]] = {}
            for message in profile_messages:
                code = message.code or "-"
                if code not in messages_based_on_codes:
                    messages_based_on_codes[code] = []
                messages_based_on_codes[code].append(message)

            for code, messages in messages_based_on_codes.items():
                for idx, message in enumerate(messages):
                    if idx > max_same_error_code:
                        break
                    type_ = message.message_type.name
                    logger.info(
                        "%s\t%s\t%s\t%s",
                        type_,
                        message.code or "-",
                        message.source,
                        message.message,
                    )
                if len(messages) > max_same_error_code:
                    logger.info(
                        "%s\t%s\tTotal error message count: %s. Skipping others.",
                        type_,
                        code,
                        len(messages),
                    )
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
            break
