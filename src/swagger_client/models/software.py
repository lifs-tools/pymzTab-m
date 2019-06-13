# coding: utf-8

"""
    mzTab validation API.

    This is an mzTab validation service.  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: nils.hoffmann@isas.de
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from swagger_client.models.indexed_element import IndexedElement  # noqa: F401,E501
from swagger_client.models.parameter import Parameter  # noqa: F401,E501


class Software(object):
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
        'parameter': 'Parameter',
        'setting': 'list[str]'
    }

    attribute_map = {
        'parameter': 'parameter',
        'setting': 'setting'
    }

    def __init__(self, parameter=None, setting=None):  # noqa: E501
        """Software - a model defined in Swagger"""  # noqa: E501

        self._parameter = None
        self._setting = None
        self.discriminator = None

        if parameter is not None:
            self.parameter = parameter
        if setting is not None:
            self.setting = setting

    @property
    def parameter(self):
        """Gets the parameter of this Software.  # noqa: E501


        :return: The parameter of this Software.  # noqa: E501
        :rtype: Parameter
        """
        return self._parameter

    @parameter.setter
    def parameter(self, parameter):
        """Sets the parameter of this Software.


        :param parameter: The parameter of this Software.  # noqa: E501
        :type: Parameter
        """

        self._parameter = parameter

    @property
    def setting(self):
        """Gets the setting of this Software.  # noqa: E501

        A software setting used. This field MAY occur multiple times for a single software. The value of this field is deliberately set as a String, since there currently do not exist cvParams for every possible setting.  # noqa: E501

        :return: The setting of this Software.  # noqa: E501
        :rtype: list[str]
        """
        return self._setting

    @setting.setter
    def setting(self, setting):
        """Sets the setting of this Software.

        A software setting used. This field MAY occur multiple times for a single software. The value of this field is deliberately set as a String, since there currently do not exist cvParams for every possible setting.  # noqa: E501

        :param setting: The setting of this Software.  # noqa: E501
        :type: list[str]
        """

        self._setting = setting

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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Software):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
    def to_lines(self):
#             'parameter': 'Parameter',
#         'setting': 'list[str]'
        lines= []
        if self.parameter: lines += ['\t{}'.format(self.parameter.as_line())]
        for idx, e in enumerate(self.setting,1):
            lines += ['-setting[{}]\t{}'.format(idx, e)]
        return lines
    
    @staticmethod
    def fromText(lines):
        import re
        parameter_li = None
        setting_li = None
        
        for l in lines:
            if l.startswith('-setting'):
                if not setting_li: setting_li = []
                setting_li.append(l)
            else: # is the parameter
                parameter_li = l
        
            
        setting = None
        for s in setting_li:
            s_li = re.match(r'-setting\[\d+\](.*)', s).group(1).strip()
            if not setting: setting = []
            setting.append(s_li)
            
        kwargs = {
        'parameter': Parameter.fromText(parameter_li),
        'setting': setting,
        }
        return Software(**kwargs)
