import json
import logging
from importlib import resources
from pathlib import Path

from jsonprofile.profile import JsonProfile, validate_profile_file

import mztab_m_io
from mztab_m_io.profile.default_profile import DEFAULT_PROFILE
from mztab_m_io.profile.full_profile import FULL_PROFILE
from mztab_m_io.profile.metabolights_profile import METABOLIGHTS_PROFILE
from mztab_m_io.profile.mtd_smf_profile import MTD_SMF_PROFILE
from mztab_m_io.profile.mtd_sml_profile import MTD_SML_PROFILE
from scripts.utils import setup_basic_logging_config

logger = logging.getLogger(__name__)

profiles_file_path = Path(
    resources.files(mztab_m_io.__name__).joinpath("resources/profiles")
)


def update_schema_file():
    profile_schema_json = JsonProfile.model_json_schema(
        by_alias=True, mode="serialization"
    )

    profile_schema_path = profiles_file_path / Path(
        "mztabm-profile-2.1.0-M.schema.json"
    )
    with profile_schema_path.open("w") as f:
        json.dump(profile_schema_json, f, indent=4)


def update_profile_file(profile: JsonProfile, filename: None | str = None):
    if not filename:
        filename = Path(profile.id).name
    profiles_file_path.mkdir(exist_ok=True, parents=True)
    profile_path = profiles_file_path / Path(filename)

    with profile_path.open("w") as f:
        json.dump(profile.model_dump(exclude_none=True), f, indent=4)
    valid, messages = validate_profile_file(profile_path)
    valid_message = "Valid" if valid else "Invalid"
    logger.info("%s profile file: %s", valid_message, profile_path)
    for message in messages:
        type_ = message.enforcement_level.name
        logger.info(
            "%s\t%s (%s): %s",
            type_,
            message.code or "-",
            message.source,
            message.message,
        )

    logger.info("Profile '%s' saved on %s", profile.id, profile_path)


if __name__ == "__main__":
    setup_basic_logging_config()
    update_schema_file()
    for profile in [
        DEFAULT_PROFILE,
        MTD_SML_PROFILE,
        MTD_SMF_PROFILE,
        FULL_PROFILE,
        METABOLIGHTS_PROFILE,
    ]:
        update_profile_file(profile)
