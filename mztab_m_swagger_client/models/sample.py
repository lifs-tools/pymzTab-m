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


class Sample(object):
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
        'species': 'list[Parameter]',
        'tissue': 'list[Parameter]',
        'cell_type': 'list[Parameter]',
        'disease': 'list[Parameter]',
        'description': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'custom': 'custom',
        'species': 'species',
        'tissue': 'tissue',
        'cell_type': 'cell_type',
        'disease': 'disease',
        'description': 'description'
    }

    def __init__(self, id=None, name=None, custom=None, species=None, tissue=None, cell_type=None, disease=None, description=None, local_vars_configuration=None):  # noqa: E501
        """Sample - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._custom = None
        self._species = None
        self._tissue = None
        self._cell_type = None
        self._disease = None
        self._description = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if custom is not None:
            self.custom = custom
        if species is not None:
            self.species = species
        if tissue is not None:
            self.tissue = tissue
        if cell_type is not None:
            self.cell_type = cell_type
        if disease is not None:
            self.disease = disease
        if description is not None:
            self.description = description

    @property
    def id(self):
        """Gets the id of this Sample.  # noqa: E501


        :return: The id of this Sample.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Sample.


        :param id: The id of this Sample.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                id is not None and id < 1):  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a value greater than or equal to `1`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this Sample.  # noqa: E501

        The sample's name.  # noqa: E501

        :return: The name of this Sample.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Sample.

        The sample's name.  # noqa: E501

        :param name: The name of this Sample.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def custom(self):
        """Gets the custom of this Sample.  # noqa: E501

        Additional user or cv parameters.  # noqa: E501

        :return: The custom of this Sample.  # noqa: E501
        :rtype: list[Parameter]
        """
        return self._custom

    @custom.setter
    def custom(self, custom):
        """Sets the custom of this Sample.

        Additional user or cv parameters.  # noqa: E501

        :param custom: The custom of this Sample.  # noqa: E501
        :type: list[Parameter]
        """

        self._custom = custom

    @property
    def species(self):
        """Gets the species of this Sample.  # noqa: E501

        Biological species information on the sample.  # noqa: E501

        :return: The species of this Sample.  # noqa: E501
        :rtype: list[Parameter]
        """
        return self._species

    @species.setter
    def species(self, species):
        """Sets the species of this Sample.

        Biological species information on the sample.  # noqa: E501

        :param species: The species of this Sample.  # noqa: E501
        :type: list[Parameter]
        """

        self._species = species

    @property
    def tissue(self):
        """Gets the tissue of this Sample.  # noqa: E501

        Biological tissue information on the sample.  # noqa: E501

        :return: The tissue of this Sample.  # noqa: E501
        :rtype: list[Parameter]
        """
        return self._tissue

    @tissue.setter
    def tissue(self, tissue):
        """Sets the tissue of this Sample.

        Biological tissue information on the sample.  # noqa: E501

        :param tissue: The tissue of this Sample.  # noqa: E501
        :type: list[Parameter]
        """

        self._tissue = tissue

    @property
    def cell_type(self):
        """Gets the cell_type of this Sample.  # noqa: E501

        Biological cell type information on the sample.  # noqa: E501

        :return: The cell_type of this Sample.  # noqa: E501
        :rtype: list[Parameter]
        """
        return self._cell_type

    @cell_type.setter
    def cell_type(self, cell_type):
        """Sets the cell_type of this Sample.

        Biological cell type information on the sample.  # noqa: E501

        :param cell_type: The cell_type of this Sample.  # noqa: E501
        :type: list[Parameter]
        """

        self._cell_type = cell_type

    @property
    def disease(self):
        """Gets the disease of this Sample.  # noqa: E501

        Disease information on the sample.  # noqa: E501

        :return: The disease of this Sample.  # noqa: E501
        :rtype: list[Parameter]
        """
        return self._disease

    @disease.setter
    def disease(self, disease):
        """Sets the disease of this Sample.

        Disease information on the sample.  # noqa: E501

        :param disease: The disease of this Sample.  # noqa: E501
        :type: list[Parameter]
        """

        self._disease = disease

    @property
    def description(self):
        """Gets the description of this Sample.  # noqa: E501

        A free form description of the sample.  # noqa: E501

        :return: The description of this Sample.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Sample.

        A free form description of the sample.  # noqa: E501

        :param description: The description of this Sample.  # noqa: E501
        :type: str
        """

        self._description = description

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
        if not isinstance(other, Sample):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Sample):
            return True

        return self.to_dict() != other.to_dict()
