import logging
import traceback

from mztab_m_io import MzTabMLoadResult, convert_to_dict, read

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    file_path = "tests/data/example/example.mztab"
    try:
        result: MzTabMLoadResult = read(file_path)
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        exit(1)

    for message in result.messages:
        logger.info("%s: %s", message.message_type.name, message.message)
    if not result.success:
        exit(1)
    mztabm_dict = convert_to_dict(result.mztabm)
    data = result.mztabm
