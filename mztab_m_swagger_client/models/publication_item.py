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


class PublicationItem(object):
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
        'type': 'str',
        'accession': 'str'
    }

    attribute_map = {
        'type': 'type',
        'accession': 'accession'
    }

    def __init__(self, type='doi', accession=None, local_vars_configuration=None):  # noqa: E501
        """PublicationItem - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._type = None
        self._accession = None
        self.discriminator = None

        self.type = type
        self.accession = accession

    @property
    def type(self):
        """Gets the type of this PublicationItem.  # noqa: E501

        The type qualifier of this publication item.  # noqa: E501

        :return: The type of this PublicationItem.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this PublicationItem.

        The type qualifier of this publication item.  # noqa: E501

        :param type: The type of this PublicationItem.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["doi", "pubmed", "uri"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def accession(self):
        """Gets the accession of this PublicationItem.  # noqa: E501

        The native accession id for this publication item.  # noqa: E501

        :return: The accession of this PublicationItem.  # noqa: E501
        :rtype: str
        """
        return self._accession

    @accession.setter
    def accession(self, accession):
        """Sets the accession of this PublicationItem.

        The native accession id for this publication item.  # noqa: E501

        :param accession: The accession of this PublicationItem.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and accession is None:  # noqa: E501
            raise ValueError("Invalid value for `accession`, must not be `None`")  # noqa: E501

        self._accession = accession

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
        if not isinstance(other, PublicationItem):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PublicationItem):
            return True

        return self.to_dict() != other.to_dict()
