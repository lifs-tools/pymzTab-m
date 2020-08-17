# coding: utf-8

"""
    mzTab-M reference implementation and validation API.

    This is the mzTab-M reference implementation and validation API service.  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: nils.hoffmann@isas.de
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import mztab_m_swagger_client
from mztab_m_swagger_client.models.publication_item import PublicationItem  # noqa: E501
from mztab_m_swagger_client.rest import ApiException

class TestPublicationItem(unittest.TestCase):
    """PublicationItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PublicationItem
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = mztab_m_swagger_client.models.publication_item.PublicationItem()  # noqa: E501
        if include_optional :
            return PublicationItem(
                type = 'doi', 
                accession = '0'
            )
        else :
            return PublicationItem(
                type = 'doi',
                accession = '0',
        )

    def testPublicationItem(self):
        """Test PublicationItem"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
