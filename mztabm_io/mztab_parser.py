import re
import pandas as pd

import mztabm_client
from mztabm_client.models.comment import Comment
from mztabm_client.models.metadata import Metadata
from mztabm_client.models.mz_tab import MzTab
from mztabm_client.models.parameter import Parameter
from mztabm_client.models.small_molecule_evidence import SmallMoleculeEvidence
from mztabm_client.models.small_molecule_feature import SmallMoleculeFeature
from mztabm_client.models.small_molecule_summary import SmallMoleculeSummary

def parseComments(text):
    comments = []
    lines = text.splitlines()
    p = re.compile(r'^COM\t(.*)$') # does not strip
    
    for idx, l in enumerate(lines):
        m = re.match(p,l)
        if m:
            msg = m.groups()[0]
            c = Comment('COM', msg.strip(), idx+1)
            comments.append(c)
    return comments

def lines_with_Header(header, text):
    header_lines = []
    lines = text.splitlines()
    p = re.compile(r'^'+header+r'\t(.+)')
    
    for idx, l in enumerate(lines):
        m = re.match(p,l)
        if m:
            text = m.groups()[0]
            text.strip()
            header_lines.append(text)
    
    return header_lines

def get_str(k,lines):
    res = None
    p = re.compile(r'^'+k+r'\t(.*)$')
    for l in lines:
        m = re.match(p,l)
        if m:
            res = m.groups()[0]
            res = res.strip()
            break
    return res

def get_parameter(k,lines):
    res = None
    p = re.compile(r'^'+k+r'\t(.*)$')
    for l in lines:
        m = re.match(p,l)
        if m:
            res = m.groups()[0]
            res = res.strip()
            res = parameter_from_text(res)
            break
    return res

def parameter_from_text(text):
    parts = text.split(',')
    return Parameter(id=None, cv_label=parts[0], cv_accession=parts[1], name=parts[2], value=parts[3])

def get_list_of(klass,k,lines):
    res = []
    intermediate = {}
    p = re.compile(r'^'+k+r'\[(\d+)\](.*)$')
    
    for l in lines:
        m = re.match(p,l)
        if m:
            idx = m.groups()[0]
            rest = m.groups()[1].strip()
            if rest.startswith('-'):# its a sublist
                if idx not in  intermediate: intermediate[idx]=[]
                elif isinstance(intermediate[idx],str):# sublist started with no sublist
                    item = intermediate[idx]
                    intermediate[idx] = []
                    intermediate[idx].append(item)
                intermediate[idx].append(rest)
            else:
                intermediate[idx]=rest
    
    for i,text in intermediate.items():
        res.append(klass.fromText(text))
        
    return res

def parseMetadata(text):
    lines =  lines_with_Header('MTD', text)
    
    kwargs={}
    
    for k,v in Metadata.openapi_types.items():
        attr = Metadata.attribute_map[k]
        if v=='str':
            kwargs[k]= get_str(attr,lines)
        elif v=='Parameter':
            kwargs[k]= get_parameter(attr,lines)
        elif v.startswith('list['):
            sub_kls = re.match(r'list\[(.*)\]', v).group(1)
            klass = getattr(mztabm_client.models, sub_kls) 
            kwargs[k]= get_list_of(klass,attr,lines)
        else:
            kwargs[k]=None
    return kwargs

def parseMetadata_as_pandas(text, start_row, end_row):
    import sys
    if sys.version_info[0] < 3: 
        from StringIO import StringIO
    else:
        from io import StringIO
    
    df = pd.read_csv(StringIO(text), sep='\t', header=None, skiprows=start_row, nrows=end_row-start_row)
    
    mtd_df = df[df[0] =='MTD']
    mtd_df.columns = list("Key","Value")
    return mtd_df

def parseSmall_molecule_summary(text, start_row, end_row):

    offsets = find_section_offsets(text)
    
    sml_df, headers = parseSmall_molecule_summary_as_pandas(text, start_row, end_row)
    
    items = []
    
    for tup in sml_df.itertuples(): # we need the headers because they are renamed
        items.append(SmallMoleculeSummary.fromTuple(tup, headers))
    
    return items

def parseSmall_molecule_summary_as_pandas(text, start_row, end_row):
    import sys
    if sys.version_info[0] < 3: 
        from StringIO import StringIO
    else:
        from io import StringIO

    # scan for the header lines
    
    df = pd.read_csv(StringIO(text), sep='\t', header=None, skiprows=start_row, nrows=end_row-start_row)
    
    headers =  df[df[0] =='SMH'].squeeze()
    headers.index = headers.index +1 # got the index column
    sml_df = df[df[0] =='SML']
    sml_df.columns = headers.tolist()
    return sml_df, headers

def parseSmall_molecule_feature(text, start_row, end_row):

    smf_df, headers = parseSmall_molecule_feature_as_pandas(text)
    
    items = []
    
    for tup in smf_df.itertuples(): # we need the headers because they are renamed
        items.append(SmallMoleculeFeature.fromTuple(tup, headers))
    
    return items

def parseSmall_molecule_feature_as_pandas(text, start_row, end_row):
    import sys
    if sys.version_info[0] < 3: 
        from StringIO import StringIO
    else:
        from io import StringIO
    
    df = pd.read_csv(StringIO(text), sep='\t', header=None, skiprows=start_row, nrows=end_row-start_row)
    
    headers =  df[df[0] =='SFH'].squeeze()
    headers.index = headers.index +1 # got the index column
    smf_df = df[df[0] =='SMF']
    smf_df.columns = headers.tolist()
    return smf_df, headers

def parseSmall_molecule_evidence(text, start_row, end_row):
    
    sme_df, headers = parseSmall_molecule_evidence_as_pandas(text, start_row, end_row)
    
    items = []
    
    for tup in sme_df.itertuples(): # we need the headers because they are renamed
        items.append(SmallMoleculeEvidence.fromTuple(tup, ['index']+headers))
    
    return items

def parseSmall_molecule_evidence_as_pandas(text, start_row, end_row):
    import sys
    if sys.version_info[0] < 3: 
        from StringIO import StringIO
    else:
        from io import StringIO
    
    df = pd.read_csv(StringIO(text), sep='\t', header=None, skiprows=start_row, nrows=end_row-start_row)
    
    headers =  df[df[0] =='SEH'].squeeze()
    headers.index = headers.index +1 # got the index column
    sme_df = df[df[0] =='SME']
    sme_df.columns = headers.tolist()
    return sme_df, headers

def parse_as_pandas_from_file(file):
    offsets = find_section_offsets_in_file(file)
    mtd_df = parseMetadata_as_pandas(file, offsets['MTD'], offsets['SML'])
    sml_df = parseSmall_molecule_summary_as_pandas(file, offsets['SML'], offsets['SMF'])
    smf_df = parseSmall_molecule_feature_as_pandas(file, offsets['SMF'], offsets['SME'])
    sme_df = parseSmall_molecule_evidence_as_pandas(file, offsets['SME'], file.nlines())
    return { "MTD": mtd_df, "SML": sml_df, "SMF": smf_df, "SME": sme_df}

def parse_as_pandas(text):
    offsets = find_section_offsets(text)
    mtd_df = parseMetadata_as_pandas(text, offsets['MTD'], offsets['SML'])
    sml_df = parseSmall_molecule_summary_as_pandas(text, offsets['SML'], offsets['SMF'])
    smf_df = parseSmall_molecule_feature_as_pandas(text, offsets['SMF'], offsets['SME'])
    sme_df = parseSmall_molecule_evidence_as_pandas(text, offsets['SME'], len(text.splitlines()))
    return { "MTD": mtd_df, "SML": sml_df, "SMF": smf_df, "SME": sme_df}

def parse(text):
    
    kwargs = {
        'metadata': parseMetadata(text),
        'small_molecule_summary': parseSmall_molecule_summary(text),
        'small_molecule_feature': parseSmall_molecule_feature(text),
        'small_molecule_evidence': parseSmall_molecule_evidence(text),
        'comment': parseComments(text)
    }
    
    return MzTab(**kwargs)

def find_section_offsets_in_file(file):
    offsets = {}
    with open(file, encoding="UTF8") as f:
        for idx, line in enumerate(f):
            if line.startswith('MTD'):
                offsets['MTD'] = idx
            elif line.startswith('SML'):
                offsets['SML'] = idx
            elif line.startswith('SMF'):
                offsets['SMF'] = idx
            elif line.startswith('SME'):
                offsets['SME'] = idx
    return offsets 

# def read_file_section(file, start, end):
#     with open(file) as f:
#         lines = f.readlines()
#         return ''.join(lines[start:end])

def find_section_offsets(text):
    offsets = {}
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith('MTD'):
            offsets['MTD'] = idx
        elif line.startswith('SML'):
            offsets['SML'] = idx
        elif line.startswith('SMF'):
            offsets['SMF'] = idx
        elif line.startswith('SME'):
            offsets['SME'] = idx
    return offsets
