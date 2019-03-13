==========
Reporting
==========

Report.yml
----------

template
~~~~~~~~

download
~~~~~~~~
The ``download`` entry for a section allows you to specify files that need to be downloaded from either a web URL or
from a pipeline job from the pipeline the report will run in.
For the latter, the path is of the form ``protocol://<name of CI job>/<path to file>``, e.g. ``gitlab://test/output/t.png``
will download ``output/t.png`` from the Gitlab CI pipeline job ``test``.

The entry in the Report.yml can then be written as

.. code-block:: yaml

  download:
    <output path>: <url>
    images/t.png: gitlab://test/output/t.png
