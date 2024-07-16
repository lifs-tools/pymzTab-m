'''
Created on 11.12.2018

@author: mirandaa
'''
import unittest
import json
from collections import namedtuple
from pprint import pprint
from mztabm_io import mztab_parser
from pathlib import Path, PurePath

from mztabm_client.api_client import ApiClient


class MzTabParseTestCase(unittest.TestCase):

    def setUp(self):
        self.datapath = PurePath(Path(__file__).parents[1].absolute(), Path('data'))

    def testJsonToModelToJson(self):
        file_path = PurePath(self.datapath, 'lipidomics-example.mzTab.json')
        with open(file_path, 'r', encoding="UTF8") as jsonfile:
            txt = jsonfile.read().replace('\n', '')
        Response = namedtuple('Response', 'data')
        response = Response(txt)

        apiclient = ApiClient()
        my_mztab =  apiclient.deserialize(response_text=response, response_type='MzTab', content_type='application/json')
        self.assertEqual("2.0.0-M", my_mztab.metadata.mz_tab_version)
        self.assertEqual("ISAS-2018-1234", my_mztab.metadata.mz_tab_id)
        self.assertIsNone(my_mztab.metadata.title)
        self.assertEqual("Minimal proposed sample file for identification and quantification of lipids", my_mztab.metadata.description)

        my_mztab_json = apiclient.sanitize_for_serialization(my_mztab)
        s = json.dumps(my_mztab_json)
        s = s.replace('\n','').replace('E','e').replace(' ','').replace('e-0','e-') #dirty hack to because exponentials get upper case e
        txt = txt.replace('\n','').replace('E','e').replace(' ','').replace('e-0','e-')
        self.assertNotEqual(s, txt)

    def testMzTabParsingFromText(self):
        file_path = PurePath(self.datapath, 'lipidomics-example.mzTab')
        with open(file_path, 'r', encoding="UTF8") as f:
            text = f.read()

        res = mztab_parser.parse(text)
        pprint(res)
        self.assertNotEqual('', res)
