import re
import swagger_client.models
from swagger_client.models import *

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
            res = Parameter.fromText(res)
            break
    return res

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
    
    for k,v in Metadata.swagger_types.items():
        attr = Metadata.attribute_map[k]
        if v=='str':
            kwargs[k]= get_str(attr,lines)
        elif v=='Parameter':
            kwargs[k]= get_parameter(attr,lines)
        elif v.startswith('list['):
            sub_kls = re.match(r'list\[(.*)\]', v).group(1)
            klass = getattr(swagger_client.models, sub_kls) 
            kwargs[k]= get_list_of(klass,attr,lines)
        else:
            kwargs[k]=None
    return kwargs

def parseSmall_molecule_summary(text):
    import sys
    if sys.version_info[0] < 3: 
        from StringIO import StringIO
    else:
        from io import StringIO
        
    import pandas as pd
    
    df = pd.read_csv(StringIO(text), sep='\t', header=None)
    
    headers =  df[df[0] =='SMH'].squeeze()
    headers.index = headers.index +1 # got the index column
    sml_df = df[df[0] =='SML']
    sml_df.columns = headers.tolist()
    
    items = []
    
    for tup in sml_df.itertuples(): # we need the headers because they are renamed
        items.append(SmallMoleculeSummary.fromTuple(tup, headers))
    
    return items

def parseSmall_molecule_feature(text):
    import sys
    if sys.version_info[0] < 3: 
        from StringIO import StringIO
    else:
        from io import StringIO
        
    import pandas as pd
    
    df = pd.read_csv(StringIO(text), sep='\t', header=None)
    
    headers =  df[df[0] =='SFH'].squeeze()
    headers.index = headers.index +1 # got the index column
    sml_df = df[df[0] =='SMF']
    sml_df.columns = headers.tolist()
    
    items = []
    
    for tup in sml_df.itertuples(): # we need the headers because they are renamed
        items.append(SmallMoleculeFeature.fromTuple(tup, headers))
    
    return items

def parseSmall_molecule_evidence(text):
    import sys
    if sys.version_info[0] < 3: 
        from StringIO import StringIO
    else:
        from io import StringIO
        
    import pandas as pd
    
    df = pd.read_csv(StringIO(text), sep='\t', header=None)
    
    headers =  df[df[0] =='SEH'].squeeze()
    headers.index = headers.index +1 # got the index column
    sml_df = df[df[0] =='SME']
    sml_df.columns = headers.tolist()
    
    items = []
    
    for tup in sml_df.itertuples(): # we need the headers because they are renamed
        items.append(SmallMoleculeEvidence.fromTuple(tup, ['index']+headers))
    
    return items

def parse(text):
    
    kwargs = {
        'metadata': parseMetadata(text),
        'small_molecule_summary': parseSmall_molecule_summary(text),
        'small_molecule_feature': parseSmall_molecule_feature(text),
        'small_molecule_evidence': parseSmall_molecule_evidence(text),
        'comment': parseComments(text)
    }
    
    return MzTab(**kwargs)
    
