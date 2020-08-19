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


class SmallMoleculeSummary(object):
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
        'prefix': 'str',
        'header_prefix': 'str',
        'sml_id': 'int',
        'smf_id_refs': 'list[int]',
        'database_identifier': 'list[str]',
        'chemical_formula': 'list[str]',
        'smiles': 'list[str]',
        'inchi': 'list[str]',
        'chemical_name': 'list[str]',
        'uri': 'list[str]',
        'theoretical_neutral_mass': 'list[float]',
        'adduct_ions': 'list[str]',
        'reliability': 'str',
        'best_id_confidence_measure': 'Parameter',
        'best_id_confidence_value': 'float',
        'abundance_assay': 'list[float]',
        'abundance_study_variable': 'list[float]',
        'abundance_variation_study_variable': 'list[float]',
        'opt': 'list[OptColumnMapping]',
        'comment': 'list[Comment]'
    }

    attribute_map = {
        'prefix': 'prefix',
        'header_prefix': 'header_prefix',
        'sml_id': 'sml_id',
        'smf_id_refs': 'smf_id_refs',
        'database_identifier': 'database_identifier',
        'chemical_formula': 'chemical_formula',
        'smiles': 'smiles',
        'inchi': 'inchi',
        'chemical_name': 'chemical_name',
        'uri': 'uri',
        'theoretical_neutral_mass': 'theoretical_neutral_mass',
        'adduct_ions': 'adduct_ions',
        'reliability': 'reliability',
        'best_id_confidence_measure': 'best_id_confidence_measure',
        'best_id_confidence_value': 'best_id_confidence_value',
        'abundance_assay': 'abundance_assay',
        'abundance_study_variable': 'abundance_study_variable',
        'abundance_variation_study_variable': 'abundance_variation_study_variable',
        'opt': 'opt',
        'comment': 'comment'
    }

    def __init__(self, prefix='SML', header_prefix='SMH', sml_id=None, smf_id_refs=None, database_identifier=None, chemical_formula=None, smiles=None, inchi=None, chemical_name=None, uri=None, theoretical_neutral_mass=None, adduct_ions=None, reliability=None, best_id_confidence_measure=None, best_id_confidence_value=None, abundance_assay=None, abundance_study_variable=None, abundance_variation_study_variable=None, opt=None, comment=None, local_vars_configuration=None):  # noqa: E501
        """SmallMoleculeSummary - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._prefix = None
        self._header_prefix = None
        self._sml_id = None
        self._smf_id_refs = None
        self._database_identifier = None
        self._chemical_formula = None
        self._smiles = None
        self._inchi = None
        self._chemical_name = None
        self._uri = None
        self._theoretical_neutral_mass = None
        self._adduct_ions = None
        self._reliability = None
        self._best_id_confidence_measure = None
        self._best_id_confidence_value = None
        self._abundance_assay = None
        self._abundance_study_variable = None
        self._abundance_variation_study_variable = None
        self._opt = None
        self._comment = None
        self.discriminator = None

        if prefix is not None:
            self.prefix = prefix
        if header_prefix is not None:
            self.header_prefix = header_prefix
        self.sml_id = sml_id
        if smf_id_refs is not None:
            self.smf_id_refs = smf_id_refs
        if database_identifier is not None:
            self.database_identifier = database_identifier
        if chemical_formula is not None:
            self.chemical_formula = chemical_formula
        if smiles is not None:
            self.smiles = smiles
        if inchi is not None:
            self.inchi = inchi
        if chemical_name is not None:
            self.chemical_name = chemical_name
        if uri is not None:
            self.uri = uri
        if theoretical_neutral_mass is not None:
            self.theoretical_neutral_mass = theoretical_neutral_mass
        if adduct_ions is not None:
            self.adduct_ions = adduct_ions
        if reliability is not None:
            self.reliability = reliability
        if best_id_confidence_measure is not None:
            self.best_id_confidence_measure = best_id_confidence_measure
        if best_id_confidence_value is not None:
            self.best_id_confidence_value = best_id_confidence_value
        if abundance_assay is not None:
            self.abundance_assay = abundance_assay
        if abundance_study_variable is not None:
            self.abundance_study_variable = abundance_study_variable
        if abundance_variation_study_variable is not None:
            self.abundance_variation_study_variable = abundance_variation_study_variable
        if opt is not None:
            self.opt = opt
        if comment is not None:
            self.comment = comment

    @property
    def prefix(self):
        """Gets the prefix of this SmallMoleculeSummary.  # noqa: E501

        The small molecule table row prefix. SML MUST be used for rows of the small molecule table.  # noqa: E501

        :return: The prefix of this SmallMoleculeSummary.  # noqa: E501
        :rtype: str
        """
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        """Sets the prefix of this SmallMoleculeSummary.

        The small molecule table row prefix. SML MUST be used for rows of the small molecule table.  # noqa: E501

        :param prefix: The prefix of this SmallMoleculeSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["SML"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and prefix not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `prefix` ({0}), must be one of {1}"  # noqa: E501
                .format(prefix, allowed_values)
            )

        self._prefix = prefix

    @property
    def header_prefix(self):
        """Gets the header_prefix of this SmallMoleculeSummary.  # noqa: E501

        The small molecule table header prefix. SMH MUST be used for the small molecule table header line (the column labels).  # noqa: E501

        :return: The header_prefix of this SmallMoleculeSummary.  # noqa: E501
        :rtype: str
        """
        return self._header_prefix

    @header_prefix.setter
    def header_prefix(self, header_prefix):
        """Sets the header_prefix of this SmallMoleculeSummary.

        The small molecule table header prefix. SMH MUST be used for the small molecule table header line (the column labels).  # noqa: E501

        :param header_prefix: The header_prefix of this SmallMoleculeSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["SMH"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and header_prefix not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `header_prefix` ({0}), must be one of {1}"  # noqa: E501
                .format(header_prefix, allowed_values)
            )

        self._header_prefix = header_prefix

    @property
    def sml_id(self):
        """Gets the sml_id of this SmallMoleculeSummary.  # noqa: E501

        A within file unique identifier for the small molecule.  # noqa: E501

        :return: The sml_id of this SmallMoleculeSummary.  # noqa: E501
        :rtype: int
        """
        return self._sml_id

    @sml_id.setter
    def sml_id(self, sml_id):
        """Sets the sml_id of this SmallMoleculeSummary.

        A within file unique identifier for the small molecule.  # noqa: E501

        :param sml_id: The sml_id of this SmallMoleculeSummary.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and sml_id is None:  # noqa: E501
            raise ValueError("Invalid value for `sml_id`, must not be `None`")  # noqa: E501

        self._sml_id = sml_id

    @property
    def smf_id_refs(self):
        """Gets the smf_id_refs of this SmallMoleculeSummary.  # noqa: E501

        References to all the features on which quantitation has been based (SMF elements) via referencing SMF_ID values. Multiple values SHOULD be provided as a “|” separated list. This MAY be null only if this is a Summary file.  # noqa: E501

        :return: The smf_id_refs of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[int]
        """
        return self._smf_id_refs

    @smf_id_refs.setter
    def smf_id_refs(self, smf_id_refs):
        """Sets the smf_id_refs of this SmallMoleculeSummary.

        References to all the features on which quantitation has been based (SMF elements) via referencing SMF_ID values. Multiple values SHOULD be provided as a “|” separated list. This MAY be null only if this is a Summary file.  # noqa: E501

        :param smf_id_refs: The smf_id_refs of this SmallMoleculeSummary.  # noqa: E501
        :type: list[int]
        """

        self._smf_id_refs = smf_id_refs

    @property
    def database_identifier(self):
        """Gets the database_identifier of this SmallMoleculeSummary.  # noqa: E501

        A list of “|” separated possible identifiers for the small molecule; multiple values MUST only be provided to indicate ambiguity in the identification of the molecule and not to demonstrate different identifier types for the same molecule. Alternative identifiers for the same molecule MAY be provided as optional columns.  The database identifier must be preceded by the resource description (prefix) followed by a colon, as specified in the metadata section.      A null value MAY be provided if the identification is sufficiently ambiguous as to be meaningless for reporting or the small molecule has not been identified.   # noqa: E501

        :return: The database_identifier of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[str]
        """
        return self._database_identifier

    @database_identifier.setter
    def database_identifier(self, database_identifier):
        """Sets the database_identifier of this SmallMoleculeSummary.

        A list of “|” separated possible identifiers for the small molecule; multiple values MUST only be provided to indicate ambiguity in the identification of the molecule and not to demonstrate different identifier types for the same molecule. Alternative identifiers for the same molecule MAY be provided as optional columns.  The database identifier must be preceded by the resource description (prefix) followed by a colon, as specified in the metadata section.      A null value MAY be provided if the identification is sufficiently ambiguous as to be meaningless for reporting or the small molecule has not been identified.   # noqa: E501

        :param database_identifier: The database_identifier of this SmallMoleculeSummary.  # noqa: E501
        :type: list[str]
        """

        self._database_identifier = database_identifier

    @property
    def chemical_formula(self):
        """Gets the chemical_formula of this SmallMoleculeSummary.  # noqa: E501

        A list of “|” separated potential chemical formulae of the reported compound. The number of values provided MUST match the number of entities reported under “database_identifier”, even if this leads to redundant reporting of information (i.e. if ambiguity can be resolved in the chemical formula), and the validation software will throw an error if the number of “|” symbols does not match. “null” values between bars are allowed.  This should be specified in Hill notation (EA Hill 1900), i.e. elements in the order C, H and then alphabetically all other elements. Counts of one may be omitted. Elements should be capitalized properly to avoid confusion (e.g., “CO” vs. “Co”). The chemical formula reported should refer to the neutral form.  Example: N-acetylglucosamine would be encoded by the string “C8H15NO6”.   # noqa: E501

        :return: The chemical_formula of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[str]
        """
        return self._chemical_formula

    @chemical_formula.setter
    def chemical_formula(self, chemical_formula):
        """Sets the chemical_formula of this SmallMoleculeSummary.

        A list of “|” separated potential chemical formulae of the reported compound. The number of values provided MUST match the number of entities reported under “database_identifier”, even if this leads to redundant reporting of information (i.e. if ambiguity can be resolved in the chemical formula), and the validation software will throw an error if the number of “|” symbols does not match. “null” values between bars are allowed.  This should be specified in Hill notation (EA Hill 1900), i.e. elements in the order C, H and then alphabetically all other elements. Counts of one may be omitted. Elements should be capitalized properly to avoid confusion (e.g., “CO” vs. “Co”). The chemical formula reported should refer to the neutral form.  Example: N-acetylglucosamine would be encoded by the string “C8H15NO6”.   # noqa: E501

        :param chemical_formula: The chemical_formula of this SmallMoleculeSummary.  # noqa: E501
        :type: list[str]
        """

        self._chemical_formula = chemical_formula

    @property
    def smiles(self):
        """Gets the smiles of this SmallMoleculeSummary.  # noqa: E501

        A list of “|” separated potential molecule structures in the simplified molecular-input line-entry system (SMILES) for the small molecule. The number of values provided MUST match the number of entities reported under “database_identifier”, and the validation software will throw an error if the number of “|” symbols does not match. “null” values between bars are allowed.  # noqa: E501

        :return: The smiles of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[str]
        """
        return self._smiles

    @smiles.setter
    def smiles(self, smiles):
        """Sets the smiles of this SmallMoleculeSummary.

        A list of “|” separated potential molecule structures in the simplified molecular-input line-entry system (SMILES) for the small molecule. The number of values provided MUST match the number of entities reported under “database_identifier”, and the validation software will throw an error if the number of “|” symbols does not match. “null” values between bars are allowed.  # noqa: E501

        :param smiles: The smiles of this SmallMoleculeSummary.  # noqa: E501
        :type: list[str]
        """

        self._smiles = smiles

    @property
    def inchi(self):
        """Gets the inchi of this SmallMoleculeSummary.  # noqa: E501

        A list of “|” separated potential standard IUPAC International Chemical Identifier (InChI) of the given substance.  The number of values provided MUST match the number of entities reported under “database_identifier”, even if this leads to redundant information being reported (i.e. if ambiguity can be resolved in the InChi), and the validation software will throw an error if the number of “|” symbols does not match. “null” values between bars are allowed.   # noqa: E501

        :return: The inchi of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[str]
        """
        return self._inchi

    @inchi.setter
    def inchi(self, inchi):
        """Sets the inchi of this SmallMoleculeSummary.

        A list of “|” separated potential standard IUPAC International Chemical Identifier (InChI) of the given substance.  The number of values provided MUST match the number of entities reported under “database_identifier”, even if this leads to redundant information being reported (i.e. if ambiguity can be resolved in the InChi), and the validation software will throw an error if the number of “|” symbols does not match. “null” values between bars are allowed.   # noqa: E501

        :param inchi: The inchi of this SmallMoleculeSummary.  # noqa: E501
        :type: list[str]
        """

        self._inchi = inchi

    @property
    def chemical_name(self):
        """Gets the chemical_name of this SmallMoleculeSummary.  # noqa: E501

        A list of “|” separated possible chemical/common names for the small molecule, or general description if a chemical name is unavailable. Multiple names are only to demonstrate ambiguity in the identification. The number of values provided MUST match the number of entities reported under “database_identifier”, and the validation software will throw an error if the number of “|” symbols does not match. “null” values between bars are allowed.   # noqa: E501

        :return: The chemical_name of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[str]
        """
        return self._chemical_name

    @chemical_name.setter
    def chemical_name(self, chemical_name):
        """Sets the chemical_name of this SmallMoleculeSummary.

        A list of “|” separated possible chemical/common names for the small molecule, or general description if a chemical name is unavailable. Multiple names are only to demonstrate ambiguity in the identification. The number of values provided MUST match the number of entities reported under “database_identifier”, and the validation software will throw an error if the number of “|” symbols does not match. “null” values between bars are allowed.   # noqa: E501

        :param chemical_name: The chemical_name of this SmallMoleculeSummary.  # noqa: E501
        :type: list[str]
        """

        self._chemical_name = chemical_name

    @property
    def uri(self):
        """Gets the uri of this SmallMoleculeSummary.  # noqa: E501

        A URI pointing to the small molecule’s entry in a reference database (e.g., the small molecule’s HMDB or KEGG entry). The number of values provided MUST match the number of entities reported under “database_identifier”, and the validation software will throw an error if the number of “|” symbols does not match. “null” values between bars are allowed.  # noqa: E501

        :return: The uri of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[str]
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this SmallMoleculeSummary.

        A URI pointing to the small molecule’s entry in a reference database (e.g., the small molecule’s HMDB or KEGG entry). The number of values provided MUST match the number of entities reported under “database_identifier”, and the validation software will throw an error if the number of “|” symbols does not match. “null” values between bars are allowed.  # noqa: E501

        :param uri: The uri of this SmallMoleculeSummary.  # noqa: E501
        :type: list[str]
        """

        self._uri = uri

    @property
    def theoretical_neutral_mass(self):
        """Gets the theoretical_neutral_mass of this SmallMoleculeSummary.  # noqa: E501

        The small molecule’s precursor’s theoretical neutral mass.  The number of values provided MUST match the number of entities reported under “database_identifier”, and the validation software will throw an error if the number of “|” symbols does not match. “null” values (in general and between bars) are allowed for molecules that have not been identified only, or for molecules where the neutral mass cannot be calculated. In these cases, the SML entry SHOULD reference features in which exp_mass_to_charge values are captured.   # noqa: E501

        :return: The theoretical_neutral_mass of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[float]
        """
        return self._theoretical_neutral_mass

    @theoretical_neutral_mass.setter
    def theoretical_neutral_mass(self, theoretical_neutral_mass):
        """Sets the theoretical_neutral_mass of this SmallMoleculeSummary.

        The small molecule’s precursor’s theoretical neutral mass.  The number of values provided MUST match the number of entities reported under “database_identifier”, and the validation software will throw an error if the number of “|” symbols does not match. “null” values (in general and between bars) are allowed for molecules that have not been identified only, or for molecules where the neutral mass cannot be calculated. In these cases, the SML entry SHOULD reference features in which exp_mass_to_charge values are captured.   # noqa: E501

        :param theoretical_neutral_mass: The theoretical_neutral_mass of this SmallMoleculeSummary.  # noqa: E501
        :type: list[float]
        """

        self._theoretical_neutral_mass = theoretical_neutral_mass

    @property
    def adduct_ions(self):
        """Gets the adduct_ions of this SmallMoleculeSummary.  # noqa: E501

        A “|” separated list of detected adducts for this this molecule, following the general style in the 2013 IUPAC recommendations on terms relating to MS e.g. [M+H]1+, [M+Na]1+, [M+NH4]1+, [M-H]1-, [M+Cl]1-, [M+H]1+. If the adduct classification is ambiguous with regards to identification evidence it MAY be null.   # noqa: E501

        :return: The adduct_ions of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[str]
        """
        return self._adduct_ions

    @adduct_ions.setter
    def adduct_ions(self, adduct_ions):
        """Sets the adduct_ions of this SmallMoleculeSummary.

        A “|” separated list of detected adducts for this this molecule, following the general style in the 2013 IUPAC recommendations on terms relating to MS e.g. [M+H]1+, [M+Na]1+, [M+NH4]1+, [M-H]1-, [M+Cl]1-, [M+H]1+. If the adduct classification is ambiguous with regards to identification evidence it MAY be null.   # noqa: E501

        :param adduct_ions: The adduct_ions of this SmallMoleculeSummary.  # noqa: E501
        :type: list[str]
        """

        self._adduct_ions = adduct_ions

    @property
    def reliability(self):
        """Gets the reliability of this SmallMoleculeSummary.  # noqa: E501

        The reliability of the given small molecule identification. This must be supplied by the resource and MUST be reported as an integer between 1-4:      identified metabolite (1)      putatively annotated compound (2)      putatively characterized compound class (3)      unknown compound (4)  These MAY be replaced using a suitable CV term in the metadata section e.g. to use MSI recommendation levels (see Section 6.2.57 for details).  The following CV terms are already available within the PSI MS CV. Future schemes may be implemented by extending the PSI MS CV with new terms and associated levels.  The MSI has recently discussed an extension of the original four level scheme into a five level scheme MS:1002896 (compound identification confidence level) with levels      isolated, pure compound, full stereochemistry (0)      reference standard match or full 2D structure (1)      unambiguous diagnostic evidence (literature, database) (2)      most likely structure, including isomers, substance class or substructure match (3)      unknown compound (4)  For high-resolution MS, the following term and its levels may be used: MS:1002955 (hr-ms compound identification confidence level) with levels      confirmed structure (1)      probable structure (2)          unambiguous ms library match (2a)          diagnostic evidence (2b)      tentative candidates (3)      unequivocal molecular formula (4)      exact mass (5)  A String data type is set to allow for different systems to be specified in the metadata section.   # noqa: E501

        :return: The reliability of this SmallMoleculeSummary.  # noqa: E501
        :rtype: str
        """
        return self._reliability

    @reliability.setter
    def reliability(self, reliability):
        """Sets the reliability of this SmallMoleculeSummary.

        The reliability of the given small molecule identification. This must be supplied by the resource and MUST be reported as an integer between 1-4:      identified metabolite (1)      putatively annotated compound (2)      putatively characterized compound class (3)      unknown compound (4)  These MAY be replaced using a suitable CV term in the metadata section e.g. to use MSI recommendation levels (see Section 6.2.57 for details).  The following CV terms are already available within the PSI MS CV. Future schemes may be implemented by extending the PSI MS CV with new terms and associated levels.  The MSI has recently discussed an extension of the original four level scheme into a five level scheme MS:1002896 (compound identification confidence level) with levels      isolated, pure compound, full stereochemistry (0)      reference standard match or full 2D structure (1)      unambiguous diagnostic evidence (literature, database) (2)      most likely structure, including isomers, substance class or substructure match (3)      unknown compound (4)  For high-resolution MS, the following term and its levels may be used: MS:1002955 (hr-ms compound identification confidence level) with levels      confirmed structure (1)      probable structure (2)          unambiguous ms library match (2a)          diagnostic evidence (2b)      tentative candidates (3)      unequivocal molecular formula (4)      exact mass (5)  A String data type is set to allow for different systems to be specified in the metadata section.   # noqa: E501

        :param reliability: The reliability of this SmallMoleculeSummary.  # noqa: E501
        :type: str
        """

        self._reliability = reliability

    @property
    def best_id_confidence_measure(self):
        """Gets the best_id_confidence_measure of this SmallMoleculeSummary.  # noqa: E501


        :return: The best_id_confidence_measure of this SmallMoleculeSummary.  # noqa: E501
        :rtype: Parameter
        """
        return self._best_id_confidence_measure

    @best_id_confidence_measure.setter
    def best_id_confidence_measure(self, best_id_confidence_measure):
        """Sets the best_id_confidence_measure of this SmallMoleculeSummary.


        :param best_id_confidence_measure: The best_id_confidence_measure of this SmallMoleculeSummary.  # noqa: E501
        :type: Parameter
        """

        self._best_id_confidence_measure = best_id_confidence_measure

    @property
    def best_id_confidence_value(self):
        """Gets the best_id_confidence_value of this SmallMoleculeSummary.  # noqa: E501

        The best confidence measure in identification (for this type of score) for the given small molecule across all assays. The type of score MUST be defined in the metadata section. If the small molecule was not identified by the specified search engine, “null” MUST be reported. If the confidence measure does not report a numerical confidence value, “null” SHOULD be reported.  # noqa: E501

        :return: The best_id_confidence_value of this SmallMoleculeSummary.  # noqa: E501
        :rtype: float
        """
        return self._best_id_confidence_value

    @best_id_confidence_value.setter
    def best_id_confidence_value(self, best_id_confidence_value):
        """Sets the best_id_confidence_value of this SmallMoleculeSummary.

        The best confidence measure in identification (for this type of score) for the given small molecule across all assays. The type of score MUST be defined in the metadata section. If the small molecule was not identified by the specified search engine, “null” MUST be reported. If the confidence measure does not report a numerical confidence value, “null” SHOULD be reported.  # noqa: E501

        :param best_id_confidence_value: The best_id_confidence_value of this SmallMoleculeSummary.  # noqa: E501
        :type: float
        """

        self._best_id_confidence_value = best_id_confidence_value

    @property
    def abundance_assay(self):
        """Gets the abundance_assay of this SmallMoleculeSummary.  # noqa: E501

        The small molecule’s abundance in every assay described in the metadata section MUST be reported. Null or zero values may be reported as appropriate. \"null\" SHOULD be used to report missing quantities, while zero SHOULD be used to indicate a present but not reliably quantifiable value (e.g. below a minimum noise threshold).  # noqa: E501

        :return: The abundance_assay of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[float]
        """
        return self._abundance_assay

    @abundance_assay.setter
    def abundance_assay(self, abundance_assay):
        """Sets the abundance_assay of this SmallMoleculeSummary.

        The small molecule’s abundance in every assay described in the metadata section MUST be reported. Null or zero values may be reported as appropriate. \"null\" SHOULD be used to report missing quantities, while zero SHOULD be used to indicate a present but not reliably quantifiable value (e.g. below a minimum noise threshold).  # noqa: E501

        :param abundance_assay: The abundance_assay of this SmallMoleculeSummary.  # noqa: E501
        :type: list[float]
        """

        self._abundance_assay = abundance_assay

    @property
    def abundance_study_variable(self):
        """Gets the abundance_study_variable of this SmallMoleculeSummary.  # noqa: E501

        The small molecule’s abundance in all the study variables described in the metadata section (study_variable[1-n]_average_function), calculated using the method as described in the Metadata section (default = arithmetic mean across assays). Null or zero values may be reported as appropriate. \"null\" SHOULD be used to report missing quantities, while zero SHOULD be used to indicate a present but not reliably quantifiable value (e.g. below a minimum noise threshold).  # noqa: E501

        :return: The abundance_study_variable of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[float]
        """
        return self._abundance_study_variable

    @abundance_study_variable.setter
    def abundance_study_variable(self, abundance_study_variable):
        """Sets the abundance_study_variable of this SmallMoleculeSummary.

        The small molecule’s abundance in all the study variables described in the metadata section (study_variable[1-n]_average_function), calculated using the method as described in the Metadata section (default = arithmetic mean across assays). Null or zero values may be reported as appropriate. \"null\" SHOULD be used to report missing quantities, while zero SHOULD be used to indicate a present but not reliably quantifiable value (e.g. below a minimum noise threshold).  # noqa: E501

        :param abundance_study_variable: The abundance_study_variable of this SmallMoleculeSummary.  # noqa: E501
        :type: list[float]
        """

        self._abundance_study_variable = abundance_study_variable

    @property
    def abundance_variation_study_variable(self):
        """Gets the abundance_variation_study_variable of this SmallMoleculeSummary.  # noqa: E501

        A measure of the variability of the study variable abundance measurement, calculated using the method as described in the metadata section (study_variable[1-n]_average_function), with a default = arithmethic co-efficient of variation of the small molecule’s abundance in the given study variable.  # noqa: E501

        :return: The abundance_variation_study_variable of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[float]
        """
        return self._abundance_variation_study_variable

    @abundance_variation_study_variable.setter
    def abundance_variation_study_variable(self, abundance_variation_study_variable):
        """Sets the abundance_variation_study_variable of this SmallMoleculeSummary.

        A measure of the variability of the study variable abundance measurement, calculated using the method as described in the metadata section (study_variable[1-n]_average_function), with a default = arithmethic co-efficient of variation of the small molecule’s abundance in the given study variable.  # noqa: E501

        :param abundance_variation_study_variable: The abundance_variation_study_variable of this SmallMoleculeSummary.  # noqa: E501
        :type: list[float]
        """

        self._abundance_variation_study_variable = abundance_variation_study_variable

    @property
    def opt(self):
        """Gets the opt of this SmallMoleculeSummary.  # noqa: E501

        Additional columns can be added to the end of the small molecule table. These column headers MUST start with the prefix “opt_” followed by the {identifier} of the object they reference: assay, study variable, MS run or “global” (if the value relates to all replicates). Column names MUST only contain the following characters: ‘A’-‘Z’, ‘a’-‘z’, ‘0’-‘9’, ‘’, ‘-’, ‘[’, ‘]’, and ‘:’. CV parameter accessions MAY be used for optional columns following the format: opt{identifier}_cv_{accession}_\\{parameter name}. Spaces within the parameter’s name MUST be replaced by ‘_’.   # noqa: E501

        :return: The opt of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[OptColumnMapping]
        """
        return self._opt

    @opt.setter
    def opt(self, opt):
        """Sets the opt of this SmallMoleculeSummary.

        Additional columns can be added to the end of the small molecule table. These column headers MUST start with the prefix “opt_” followed by the {identifier} of the object they reference: assay, study variable, MS run or “global” (if the value relates to all replicates). Column names MUST only contain the following characters: ‘A’-‘Z’, ‘a’-‘z’, ‘0’-‘9’, ‘’, ‘-’, ‘[’, ‘]’, and ‘:’. CV parameter accessions MAY be used for optional columns following the format: opt{identifier}_cv_{accession}_\\{parameter name}. Spaces within the parameter’s name MUST be replaced by ‘_’.   # noqa: E501

        :param opt: The opt of this SmallMoleculeSummary.  # noqa: E501
        :type: list[OptColumnMapping]
        """

        self._opt = opt

    @property
    def comment(self):
        """Gets the comment of this SmallMoleculeSummary.  # noqa: E501


        :return: The comment of this SmallMoleculeSummary.  # noqa: E501
        :rtype: list[Comment]
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this SmallMoleculeSummary.


        :param comment: The comment of this SmallMoleculeSummary.  # noqa: E501
        :type: list[Comment]
        """

        self._comment = comment

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
        if not isinstance(other, SmallMoleculeSummary):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SmallMoleculeSummary):
            return True

        return self.to_dict() != other.to_dict()
