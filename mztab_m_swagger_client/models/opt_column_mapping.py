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


class OptColumnMapping(object):
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
        'identifier': 'str',
        'param': 'Parameter',
        'value': 'str'
    }

    attribute_map = {
        'identifier': 'identifier',
        'param': 'param',
        'value': 'value'
    }

    def __init__(self, identifier=None, param=None, value=None, local_vars_configuration=None):  # noqa: E501
        """OptColumnMapping - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._identifier = None
        self._param = None
        self._value = None
        self.discriminator = None

        self.identifier = identifier
        if param is not None:
            self.param = param
        if value is not None:
            self.value = value

    @property
    def identifier(self):
        """Gets the identifier of this OptColumnMapping.  # noqa: E501

        The fully qualified column name.  # noqa: E501

        :return: The identifier of this OptColumnMapping.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this OptColumnMapping.

        The fully qualified column name.  # noqa: E501

        :param identifier: The identifier of this OptColumnMapping.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and identifier is None:  # noqa: E501
            raise ValueError("Invalid value for `identifier`, must not be `None`")  # noqa: E501

        self._identifier = identifier

    @property
    def param(self):
        """Gets the param of this OptColumnMapping.  # noqa: E501


        :return: The param of this OptColumnMapping.  # noqa: E501
        :rtype: Parameter
        """
        return self._param

    @param.setter
    def param(self, param):
        """Sets the param of this OptColumnMapping.


        :param param: The param of this OptColumnMapping.  # noqa: E501
        :type: Parameter
        """

        self._param = param

    @property
    def value(self):
        """Gets the value of this OptColumnMapping.  # noqa: E501

        The value for this column in a particular row.  # noqa: E501

        :return: The value of this OptColumnMapping.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this OptColumnMapping.

        The value for this column in a particular row.  # noqa: E501

        :param value: The value of this OptColumnMapping.  # noqa: E501
        :type: str
        """

        self._value = value

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
        if not isinstance(other, OptColumnMapping):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OptColumnMapping):
            return True

        return self.to_dict() != other.to_dict()
