import json
import logging
import traceback
from pathlib import Path

from jsonprofile.validator.context import ValidationRuntimeConfiguration

from mztab_m_io import MzTabMLoadResult
from mztab_m_io.model.validation import Category, MzTabMessage
from mztab_m_io.profile.validator import MzTabMLoader
from scripts.utils import setup_basic_logging_config

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    setup_basic_logging_config()

    profiles = Path("mztab_m_io/resources/profiles")
    mtbls_profile_path = profiles / Path("mztabm-metabolights-profile-2.1.0-M.json")
    mtbls_profile_json = json.loads(mtbls_profile_path.read_text())

    files = list(Path("tests/data/mztabm").glob("*.mz?ab"))

    loader = MzTabMLoader(profile=mtbls_profile_json)
    max_same_error_code = 10
    runtime_config = ValidationRuntimeConfiguration(
        max_messages_for_each_requirement=5,
        skip_decimal_validations=True,
        offline_mode=False,
    )

    for idx, file_path in enumerate(files, start=1):
        try:
            logger.info("%s", 120 * "-")
            logger.info("(%s / %s) %s will be validated.", idx, len(files), file_path)
            logger.info("%s", 120 * "-")

            result: MzTabMLoadResult = loader.read(
                str(file_path), runtime_config=runtime_config
            )
            result_file_path = Path("./output") / Path(f"{file_path.name}.result.json")
            json_file_path = Path("./output") / Path(f"{file_path.name}.json")
            results_json = result.model_dump(by_alias=True)
            with result_file_path.open("w") as f:
                json.dump({"messages": results_json.get("messages", [])}, f, indent=2)
            with json_file_path.open("w") as f:
                json.dump(results_json.get("mztabm", {}), f, indent=2)

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
