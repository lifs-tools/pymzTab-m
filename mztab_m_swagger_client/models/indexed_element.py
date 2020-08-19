# coding: utf-8

"""
    mzTab-M reference implementation and validation API.

    This is the mzTab-M reference implementation and validation API service.  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: nils.hoffmann@isas.de
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class IndexedElement(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'int',
        'element_type': 'str'
    }

    attribute_map = {
        'id': 'id',
        'element_type': 'elementType'
    }

    discriminator_value_class_map = {
        'Uri': 'Uri',
        'Assay': 'Assay',
        'MsRun': 'MsRun',
        'Database': 'Database',
        'StudyVariable': 'StudyVariable',
        'SampleProcessing': 'SampleProcessing',
        'Sample': 'Sample',
        'Publication': 'Publication',
        'Contact': 'Contact',
        'CV': 'CV',
        'Instrument': 'Instrument',
        'Parameter': 'Parameter',
        'Software': 'Software'
    }

    instances_by_id = {}

    def __init__(self, id=None, element_type='element_type'):  # noqa: E501
        """IndexedElement - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._element_type = None
        self.discriminator = 'elementType'

        self.id = id
        self.element_type = element_type

        if id is not None:
            self.__class__.instances_by_id[id] = self

    @property
    def id(self):
        """Gets the id of this IndexedElement.  # noqa: E501


        :return: The id of this IndexedElement.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this IndexedElement.


        :param id: The id of this IndexedElement.  # noqa: E501
        :type: int
        """
        #if id is None:
        #    raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501
        if id is not None and id < 1:  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value greater than or equal to `1`")  # noqa: E501

        self._id = id

    @property
    def element_type(self):
        """Gets the element_type of this IndexedElement.  # noqa: E501


        :return: The element_type of this IndexedElement.  # noqa: E501
        :rtype: str
        """
        return self._element_type

    @element_type.setter
    def element_type(self, element_type):
        """Sets the element_type of this IndexedElement.


        :param element_type: The element_type of this IndexedElement.  # noqa: E501
        :type: str
        """
        if element_type is None:
            raise ValueError("Invalid value for `element_type`, must not be `None`")  # noqa: E501

        self._element_type = element_type

    def get_real_child_model(self, data):
        """Returns the real base class specified by the discriminator"""
        discriminator_value = data[self.discriminator].lower()
        return self.discriminator_value_class_map.get(discriminator_value)

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(IndexedElement, dict):
            for key, value in self.items():
                result[key] = value

        #print("IndexedElement.toDict(): ", result)
        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, IndexedElement):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
