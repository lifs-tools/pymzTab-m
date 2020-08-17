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


class MsRun(object):
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
        'location': 'str',
        'instrument_ref': 'Instrument',
        'format': 'Parameter',
        'id_format': 'Parameter',
        'fragmentation_method': 'list[Parameter]',
        'scan_polarity': 'list[Parameter]',
        'hash': 'str',
        'hash_method': 'Parameter'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'location': 'location',
        'instrument_ref': 'instrument_ref',
        'format': 'format',
        'id_format': 'id_format',
        'fragmentation_method': 'fragmentation_method',
        'scan_polarity': 'scan_polarity',
        'hash': 'hash',
        'hash_method': 'hash_method'
    }

    def __init__(self, id=None, name=None, location=None, instrument_ref=None, format=None, id_format=None, fragmentation_method=None, scan_polarity=None, hash=None, hash_method=None, local_vars_configuration=None):  # noqa: E501
        """MsRun - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._location = None
        self._instrument_ref = None
        self._format = None
        self._id_format = None
        self._fragmentation_method = None
        self._scan_polarity = None
        self._hash = None
        self._hash_method = None
        self.discriminator = None

        self.id = id
        self.name = name
        self.location = location
        if instrument_ref is not None:
            self.instrument_ref = instrument_ref
        if format is not None:
            self.format = format
        if id_format is not None:
            self.id_format = id_format
        if fragmentation_method is not None:
            self.fragmentation_method = fragmentation_method
        if scan_polarity is not None:
            self.scan_polarity = scan_polarity
        if hash is not None:
            self.hash = hash
        if hash_method is not None:
            self.hash_method = hash_method

    @property
    def id(self):
        """Gets the id of this MsRun.  # noqa: E501


        :return: The id of this MsRun.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this MsRun.


        :param id: The id of this MsRun.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                id is not None and id < 1):  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value greater than or equal to `1`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this MsRun.  # noqa: E501

        The msRun's name.  # noqa: E501

        :return: The name of this MsRun.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MsRun.

        The msRun's name.  # noqa: E501

        :param name: The name of this MsRun.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def location(self):
        """Gets the location of this MsRun.  # noqa: E501

        The msRun's location URI.  # noqa: E501

        :return: The location of this MsRun.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this MsRun.

        The msRun's location URI.  # noqa: E501

        :param location: The location of this MsRun.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and location is None:  # noqa: E501
            raise ValueError("Invalid value for `location`, must not be `None`")  # noqa: E501

        self._location = location

    @property
    def instrument_ref(self):
        """Gets the instrument_ref of this MsRun.  # noqa: E501


        :return: The instrument_ref of this MsRun.  # noqa: E501
        :rtype: Instrument
        """
        return self._instrument_ref

    @instrument_ref.setter
    def instrument_ref(self, instrument_ref):
        """Sets the instrument_ref of this MsRun.


        :param instrument_ref: The instrument_ref of this MsRun.  # noqa: E501
        :type: Instrument
        """

        self._instrument_ref = instrument_ref

    @property
    def format(self):
        """Gets the format of this MsRun.  # noqa: E501


        :return: The format of this MsRun.  # noqa: E501
        :rtype: Parameter
        """
        return self._format

    @format.setter
    def format(self, format):
        """Sets the format of this MsRun.


        :param format: The format of this MsRun.  # noqa: E501
        :type: Parameter
        """

        self._format = format

    @property
    def id_format(self):
        """Gets the id_format of this MsRun.  # noqa: E501


        :return: The id_format of this MsRun.  # noqa: E501
        :rtype: Parameter
        """
        return self._id_format

    @id_format.setter
    def id_format(self, id_format):
        """Sets the id_format of this MsRun.


        :param id_format: The id_format of this MsRun.  # noqa: E501
        :type: Parameter
        """

        self._id_format = id_format

    @property
    def fragmentation_method(self):
        """Gets the fragmentation_method of this MsRun.  # noqa: E501

        The fragmentation methods applied during this msRun.  # noqa: E501

        :return: The fragmentation_method of this MsRun.  # noqa: E501
        :rtype: list[Parameter]
        """
        return self._fragmentation_method

    @fragmentation_method.setter
    def fragmentation_method(self, fragmentation_method):
        """Sets the fragmentation_method of this MsRun.

        The fragmentation methods applied during this msRun.  # noqa: E501

        :param fragmentation_method: The fragmentation_method of this MsRun.  # noqa: E501
        :type: list[Parameter]
        """

        self._fragmentation_method = fragmentation_method

    @property
    def scan_polarity(self):
        """Gets the scan_polarity of this MsRun.  # noqa: E501

        The scan polarity/polarities used during this msRun.  # noqa: E501

        :return: The scan_polarity of this MsRun.  # noqa: E501
        :rtype: list[Parameter]
        """
        return self._scan_polarity

    @scan_polarity.setter
    def scan_polarity(self, scan_polarity):
        """Sets the scan_polarity of this MsRun.

        The scan polarity/polarities used during this msRun.  # noqa: E501

        :param scan_polarity: The scan_polarity of this MsRun.  # noqa: E501
        :type: list[Parameter]
        """

        self._scan_polarity = scan_polarity

    @property
    def hash(self):
        """Gets the hash of this MsRun.  # noqa: E501

        The file hash value of this msRun's data file.  # noqa: E501

        :return: The hash of this MsRun.  # noqa: E501
        :rtype: str
        """
        return self._hash

    @hash.setter
    def hash(self, hash):
        """Sets the hash of this MsRun.

        The file hash value of this msRun's data file.  # noqa: E501

        :param hash: The hash of this MsRun.  # noqa: E501
        :type: str
        """

        self._hash = hash

    @property
    def hash_method(self):
        """Gets the hash_method of this MsRun.  # noqa: E501


        :return: The hash_method of this MsRun.  # noqa: E501
        :rtype: Parameter
        """
        return self._hash_method

    @hash_method.setter
    def hash_method(self, hash_method):
        """Sets the hash_method of this MsRun.


        :param hash_method: The hash_method of this MsRun.  # noqa: E501
        :type: Parameter
        """

        self._hash_method = hash_method

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
        if not isinstance(other, MsRun):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MsRun):
            return True

        return self.to_dict() != other.to_dict()
