# coding: utf-8

"""
    mzTab-M reference implementation and validation API.

    This is the mzTab-M reference implementation and validation API service.  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: nils.hoffmann@isas.de
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from mztab_m_swagger_client.configuration import Configuration


class Assay(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'id': 'int',
        'name': 'str',
        'custom': 'list[Parameter]',
        'external_uri': 'str',
        'sample_ref': 'Sample',
        'ms_run_ref': 'list[MsRun]'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'custom': 'custom',
        'external_uri': 'external_uri',
        'sample_ref': 'sample_ref',
        'ms_run_ref': 'ms_run_ref'
    }

    instances_by_id = {}

    def __init__(self, id=None, name=None, custom=None, external_uri=None, sample_ref=None, ms_run_ref=None, local_vars_configuration=None):  # noqa: E501
        """Assay - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._custom = None
        self._external_uri = None
        self._sample_ref = None
        self._ms_run_ref = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.name = name
        if custom is not None:
            self.custom = custom
        if external_uri is not None:
            self.external_uri = external_uri
        if sample_ref is not None:
            self.sample_ref = sample_ref
        self.ms_run_ref = ms_run_ref

        if id is not None:
            self.__class__.instances_by_id[id] = self

    @property
    def id(self):
        """Gets the id of this Assay.  # noqa: E501


        :return: The id of this Assay.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Assay.


        :param id: The id of this Assay.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                id is not None and id < 1):  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value greater than or equal to `1`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this Assay.  # noqa: E501

        The assay name.  # noqa: E501

        :return: The name of this Assay.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Assay.

        The assay name.  # noqa: E501

        :param name: The name of this Assay.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def custom(self):
        """Gets the custom of this Assay.  # noqa: E501

        Additional user or cv parameters.  # noqa: E501

        :return: The custom of this Assay.  # noqa: E501
        :rtype: list[Parameter]
        """
        return self._custom

    @custom.setter
    def custom(self, custom):
        """Sets the custom of this Assay.

        Additional user or cv parameters.  # noqa: E501

        :param custom: The custom of this Assay.  # noqa: E501
        :type: list[Parameter]
        """

        self._custom = custom

    @property
    def external_uri(self):
        """Gets the external_uri of this Assay.  # noqa: E501

        An external URI to further information about this assay.  # noqa: E501

        :return: The external_uri of this Assay.  # noqa: E501
        :rtype: str
        """
        return self._external_uri

    @external_uri.setter
    def external_uri(self, external_uri):
        """Sets the external_uri of this Assay.

        An external URI to further information about this assay.  # noqa: E501

        :param external_uri: The external_uri of this Assay.  # noqa: E501
        :type: str
        """

        self._external_uri = external_uri

    @property
    def sample_ref(self):
        """Gets the sample_ref of this Assay.  # noqa: E501


        :return: The sample_ref of this Assay.  # noqa: E501
        :rtype: Sample
        """
        return self._sample_ref

    @sample_ref.setter
    def sample_ref(self, sample_ref):
        """Sets the sample_ref of this Assay.


        :param sample_ref: The sample_ref of this Assay.  # noqa: E501
        :type: Sample
        """

        self._sample_ref = sample_ref

    @property
    def ms_run_ref(self):
        """Gets the ms_run_ref of this Assay.  # noqa: E501

        The ms run(s) referenced by this assay.  # noqa: E501

        :return: The ms_run_ref of this Assay.  # noqa: E501
        :rtype: list[MsRun]
        """
        return self._ms_run_ref

    @ms_run_ref.setter
    def ms_run_ref(self, ms_run_ref):
        """Sets the ms_run_ref of this Assay.

        The ms run(s) referenced by this assay.  # noqa: E501

        :param ms_run_ref: The ms_run_ref of this Assay.  # noqa: E501
        :type: list[MsRun]
        """
        if self.local_vars_configuration.client_side_validation and ms_run_ref is None:  # noqa: E501
            raise ValueError("Invalid value for `ms_run_ref`, must not be `None`")  # noqa: E501

        self._ms_run_ref = ms_run_ref

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Assay):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Assay):
            return True

        return self.to_dict() != other.to_dict()
