import sys

from mztabm_client.models.mz_tab import MzTab

def writeMzTabM(file_name:str, mz_tab:MzTab):
    """Writes an mzTab object to tab-separated output.

    :param file_name: the file name to write to.
    :param mz_tab: the mz_tab object.
    """

def writeMzTabM_from_pandas_dict(file_name: str, mzTabDict: dict): 
    # open file with file_name
    with open(file_name, 'w', encoding="UTF8") as f:
        mzTabDict["MTD"].to_csv(f, sep='\t', index=False)
        f.write("\n")
        mzTabDict["SML"].to_csv(f, sep='\t', index=False)
        f.write("\n")
        mzTabDict["SMF"].to_csv(f, sep='\t', index=False)
        f.write("\n")
        mzTabDict["SME"].to_csv(f, sep='\t', index=False)
        f.write("\n")