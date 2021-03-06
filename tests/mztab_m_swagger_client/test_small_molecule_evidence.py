# coding: utf-8

"""
    mzTab-M reference implementation and validation API.

    This is the mzTab-M reference implementation and validation API service.  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: nils.hoffmann@isas.de
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re

import unittest

import mztab_m_swagger_client
from mztab_m_swagger_client.models.small_molecule_evidence import SmallMoleculeEvidence  # noqa: E501
from mztab_m_swagger_client.rest import ApiException


class TestSmallMoleculeEvidence(unittest.TestCase):
    """SmallMoleculeEvidence unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSmallMoleculeEvidence(self):
        """Test SmallMoleculeEvidence"""
        # FIXME: construct object with mandatory attributes with example values
        # model = mztab_m_swagger_client.models.small_molecule_evidence.SmallMoleculeEvidence()  # noqa: E501
        pass

    def testAdductRegex(self):
        adductIon = "[M+H]1+"
        self.assertTrue(re.fullmatch(r'^\[\d*M([+-][\w]*)\]\d*[+-]$', adductIon))

if __name__ == '__main__':
    unittest.main()
