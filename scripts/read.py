import json
import logging
import sys
import traceback
from pathlib import Path

from mztab_m_io import MzTabMLoadResult, read
from mztab_m_io.model.validation import Category
from mztab_m_io.profile.default_profile import DEFAULT_PROFILE
from mztab_m_io.profile.metabolights_profile import METABOLIGHTS_PROFILE
from mztab_m_io.profile.model import MzTabMProfile
from mztab_m_io.profile.profile_validator import validate_profile_file
from mztab_m_io.validator.mztabm_validator import MzTabMValidator

logger = logging.getLogger(__name__)


def setup_basic_logging_config(level: int = logging.INFO):
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s "
        "[%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%d/%b/%Y %H:%M:%S",
        stream=sys.stdout,
    )
    logging.getLogger("httpx2").setLevel(logging.ERROR)


if __name__ == "__main__":
    setup_basic_logging_config()
    json_schema = MzTabMProfile.model_json_schema(by_alias=True, mode="serialization")
    with Path("mztab_m_io/resources/profiles/mztabm-profile-2.1.0-M.schema.json").open(
        "w"
    ) as f:
        json.dump(json_schema, f, indent=4)
    with Path("mztab_m_io/resources/profiles/mztabm-default-profile-2.1.0-M.json").open(
        "w"
    ) as f:
        json.dump(DEFAULT_PROFILE.model_dump(exclude_none=True), f, indent=4)

    mtbls_profile = Path(
        "mztab_m_io/resources/profiles/mztabm-metabolights-profile-2.1.0-M.json"
    )
    valid, messages = validate_profile_file(mtbls_profile)

    logger.info("%s profile file: %s", "Valid" if valid else "Invalid", mtbls_profile)

    for message in messages:
        type_ = message.message_type.name
        logger.info(
            "%s\t%s (%s): %s",
            type_,
            message.code or "-",
            message.source,
            message.message,
        )
    with mtbls_profile.open("w") as f:
        json.dump(METABOLIGHTS_PROFILE.model_dump(exclude_none=True), f, indent=4)

    file_path = "tests/data/example/example.mztab"
    # file_path = "tests/data/mztabm/manual_null_MTBLS263.mztab"
    # file_path = "tests/data/mztabm/msdial_5.5.251021GUI_Height_zenodo14263441.mzTab"
    files = list(Path("tests/data/mztabm").glob("*.mz?ab"))
    profile_json = json.loads(mtbls_profile.read_text())
    validator = MzTabMValidator(profile=profile_json)
    for idx, file_path in enumerate(files, start=1):
        try:
            logger.info("%s", 120 * "-")
            logger.info("%s", 120 * "-")
            logger.info("(%s / %s) %s will be validated.", idx, len(files), file_path)
            logger.info("%s", 120 * "-")

            result: MzTabMLoadResult = read(str(file_path), validator=validator)
            profile_messages = [
                x for x in result.messages if x.category == Category.PROFILE
            ]
            for message in profile_messages:
                type_ = message.message_type.name
                logger.info(
                    "%s\t%s\t%s\t%s",
                    type_,
                    message.code or "-",
                    message.source,
                    message.message,
                )
            logger.info("%s", 120 * "-")
            logger.info("%s", 120 * "-")
        except Exception as e:
            logger.error(e)
            traceback.print_exc()

    # if not result.success:
    #     exit(1)
    # mztabm_dict = convert_to_dict(result.mztabm)
    # data = result.mztabm
