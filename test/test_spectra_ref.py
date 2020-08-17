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

import openapi_client
from openapi_client.models.spectra_ref import SpectraRef  # noqa: E501
from openapi_client.rest import ApiException

class TestSpectraRef(unittest.TestCase):
    """SpectraRef unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SpectraRef
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = openapi_client.models.spectra_ref.SpectraRef()  # noqa: E501
        if include_optional :
            return SpectraRef(
                ms_run = openapi_client.models.ms_run.MsRun(
                    id = 1, 
                    name = '0', 
                    location = '0', 
                    instrument_ref = openapi_client.models.instrument.Instrument(
                        id = 1, 
                        name = openapi_client.models.parameter.Parameter(
                            id = 1, 
                            cv_label = '0', 
                            cv_accession = '0', 
                            name = '0', 
                            value = '0', ), 
                        source = openapi_client.models.parameter.Parameter(
                            id = 1, 
                            cv_label = '0', 
                            cv_accession = '0', 
                            name = '0', 
                            value = '0', ), 
                        analyzer = [
                            openapi_client.models.parameter.Parameter(
                                id = 1, 
                                cv_label = '0', 
                                cv_accession = '0', 
                                name = '0', 
                                value = '0', )
                            ], 
                        detector = openapi_client.models.parameter.Parameter(
                            id = 1, 
                            cv_label = '0', 
                            cv_accession = '0', 
                            name = '0', 
                            value = '0', ), ), 
                    format = openapi_client.models.parameter.Parameter(
                        id = 1, 
                        cv_label = '0', 
                        cv_accession = '0', 
                        name = '0', 
                        value = '0', ), 
                    id_format = openapi_client.models.parameter.Parameter(
                        id = 1, 
                        cv_label = '0', 
                        cv_accession = '0', 
                        name = '0', 
                        value = '0', ), 
                    fragmentation_method = [
                        openapi_client.models.parameter.Parameter(
                            id = 1, 
                            cv_label = '0', 
                            cv_accession = '0', 
                            name = '0', 
                            value = '0', )
                        ], 
                    scan_polarity = [
                        openapi_client.models.parameter.Parameter(
                            id = 1, 
                            cv_label = '0', 
                            cv_accession = '0', 
                            name = '0', 
                            value = '0', )
                        ], 
                    hash = '0', 
                    hash_method = openapi_client.models.parameter.Parameter(
                        id = 1, 
                        cv_label = '0', 
                        cv_accession = '0', 
                        name = '0', 
                        value = '0', ), ), 
                reference = '0'
            )
        else :
            return SpectraRef(
                ms_run = openapi_client.models.ms_run.MsRun(
                    id = 1, 
                    name = '0', 
                    location = '0', 
                    instrument_ref = openapi_client.models.instrument.Instrument(
                        id = 1, 
                        name = openapi_client.models.parameter.Parameter(
                            id = 1, 
                            cv_label = '0', 
                            cv_accession = '0', 
                            name = '0', 
                            value = '0', ), 
                        source = openapi_client.models.parameter.Parameter(
                            id = 1, 
                            cv_label = '0', 
                            cv_accession = '0', 
                            name = '0', 
                            value = '0', ), 
                        analyzer = [
                            openapi_client.models.parameter.Parameter(
                                id = 1, 
                                cv_label = '0', 
                                cv_accession = '0', 
                                name = '0', 
                                value = '0', )
                            ], 
                        detector = openapi_client.models.parameter.Parameter(
                            id = 1, 
                            cv_label = '0', 
                            cv_accession = '0', 
                            name = '0', 
                            value = '0', ), ), 
                    format = openapi_client.models.parameter.Parameter(
                        id = 1, 
                        cv_label = '0', 
                        cv_accession = '0', 
                        name = '0', 
                        value = '0', ), 
                    id_format = openapi_client.models.parameter.Parameter(
                        id = 1, 
                        cv_label = '0', 
                        cv_accession = '0', 
                        name = '0', 
                        value = '0', ), 
                    fragmentation_method = [
                        openapi_client.models.parameter.Parameter(
                            id = 1, 
                            cv_label = '0', 
                            cv_accession = '0', 
                            name = '0', 
                            value = '0', )
                        ], 
                    scan_polarity = [
                        openapi_client.models.parameter.Parameter(
                            id = 1, 
                            cv_label = '0', 
                            cv_accession = '0', 
                            name = '0', 
                            value = '0', )
                        ], 
                    hash = '0', 
                    hash_method = openapi_client.models.parameter.Parameter(
                        id = 1, 
                        cv_label = '0', 
                        cv_accession = '0', 
                        name = '0', 
                        value = '0', ), ),
                reference = '0',
        )

    def testSpectraRef(self):
        """Test SpectraRef"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()