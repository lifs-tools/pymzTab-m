import mztab_m_swagger_client.models
from mztab_m_swagger_client.models import *
import sys

def writeMzTabM(file_name:str, mz_tab:MzTab):
    """Writes an mzTab object to tab-separated output.

    :param file_name: the file name to write to.
    :param mz_tab: the mz_tab object.
    """

def writeMzTabM_from_pandas_dict(file_name: str, mzTabDict: dict): 
    # open file with file_name
    with open(file_name, 'w') as f:
        mzTabDict["MTD"].to_csv(f, sep='\t', index=False)
        f.write("\n")
        mzTabDict["SML"].to_csv(f, sep='\t', index=False)
        f.write("\n")
        mzTabDict["SMF"].to_csv(f, sep='\t', index=False)
        f.write("\n")
        mzTabDict["SME"].to_csv(f, sep='\t', index=False)
        f.write("\n")