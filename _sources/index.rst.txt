.. pymzTab-m documentation master file, created by
   sphinx-quickstart on Fri Jun 14 09:13:59 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pymzTab-m's documentation!
=====================================

This is the mzTab-M reference implementation and validation API service for Python 3.

.. note:: This is an early development version, please use at your own risk and report issues to help improve it!

mzTab-M is intended as a reporting standard for quantitative results from metabolomics/lipodomics approaches. This format is further intended to provide local LIMS systems as well as MS metabolomics repositories a simple way to share and combine basic information.

mzTab-M has been developed with a view to support the following general tasks:

* Facilitate the sharing of final experimental results, especially with researchers outside the field of metabolomics.
* Export of results to external software, including programs such as Microsoft Excel® and Open Office Spreadsheet and statistical software / coding languages such as R and Python.
* Act as an output format of (web-) services that report MS-based results and thus can produce standardized result pages.
* Be able to link to the external experimental evidence e.g. by referencing back to mzML files.

Related Projects
================

* `mzTab-M 2.0 Standard Specification <https://github.com/HUPO-PSI/mzTab>`_
* `jmzTab-M Reference Implementation and Validator <https://github.com/lifs-tools/jmzTab-m>`_
* `jmzTab-M Webapplication and Validator <https://github.com/lifs-tools/jmzTab-m-webapp>`_


.. toctree::
   :maxdepth: 2
   :caption: Contents:

Modules
=======

* `Swagger Client <api/swagger_client.html>`_
* `mzTab Parser <api/mztab_parse.html>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`

