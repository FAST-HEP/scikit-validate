=============
scikit-validate
=============


.. image:: https://img.shields.io/pypi/v/skvalidate.svg
        :target: https://pypi.python.org/pypi/skvalidate

.. image:: https://readthedocs.org/projects/scikit-validate/badge/?version=latest
        :target: https://scikit-validate.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

* Free software: Apache Software License 2.0
* Documentation: https://scikit-validate.readthedocs.io.

Overview
--------
scikit-validate is a validation package for science output developed within `F.A.S.T.`_.
This package provides commands for monitoring and comparing analysis outputs, computing resource usage (e.g. CPU time/RAM) as well as commands for summarising findings.

Features
--------

* Collect metrics in JSON output
 * measure file metrics (e.g. size)
 * measure execution time and memory usage
 * compare to previous executions
* compare ROOT files & plot discrepancies
* create validation reports

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _`F.A.S.T.`: https://fast-hep.web.cern.ch/fast-hep/public
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
