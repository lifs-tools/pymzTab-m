'''
Created on 11.12.2018

@author: mirandaa
'''
import unittest
from swagger_client.api_client import ApiClient
import json
from collections import namedtuple
from pprint import pprint
from mzTab_Parse import mztab_parser

class MzTabParseTestCase(unittest.TestCase):

    def testJsonToModelToJson(self):
        filePath = 'data/lipidomics-example.mzTab.json'
        with open(filePath,'r') as jsonfile:
            txt = jsonfile.read().replace('\n', '')
            #-----------------
        Response = namedtuple('Response', 'data')
        response = Response(txt)

        apiclient = ApiClient()
        my_mztab = apiclient.deserialize(response,'MzTab')

        my_mztab_json = apiclient.sanitize_for_serialization(my_mztab)
        self.assertNotEqual('', my_mztab_json)
        my_mztab_text = '\n'.join(my_mztab.to_lines())
        self.assertNotEqual('', my_mztab_text)

    def testMzTabParsing(self):
        # print(my_mztab_text)

        filePath = 'data/lipidomics-example.mzTab'
        with open(filePath,'r') as f:
            text = f.read()

        res = mztab_parser.parse(text)
        pprint(res)
        self.assertNotEqual('', res)



