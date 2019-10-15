=====
Usage
=====

After installation scikit-validate will provide several commands, all starting with `sv_`:

sv_file_info
----------------------------
The first subcommand will simply record the file size of a given file and record it in a JSON file::

    sv_file_info --help
    Usage: sv_file_info [OPTIONS] [INPUT_FILES]...

    Script to record file metrics.

    For testing pick or create a file:

      # create 10 MB file     dd if=/dev/zero of=test.file bs=10485760
      count=1     sv_add_file_metrics test.file -m metrics.json

    If the output file, default metrics.json, already exists it will be read
    first and results will be appended.

    Options:
    -m, --metrics-file TEXT  file for JSON output
    --help                   Show this message and exit.

sv_execute
-------------------------------
This subcommand will execute the parameters passed to it as a shell command and monitor its resource usage.
At the moment only (simple) CPU time and RAM usage are supported::

    sv_execute --help
    Usage: sv_execute [OPTIONS] COMMAND

      Command that wraps and monitors another command.

      For testing install 'stress' package and run

          sv_execute -m resource_metrics.json -- \
                stress --cpu 1 --io 1 --vm 1 --vm-bytes 128M --timeout 10s --verbose

      If the output file, default resource_metrics.json, already exists it will
      be read first and results will be appended.

      If a single string argument is provided as the command then it will be
      split using white-space, however if multiple arguments are provided then
      no additional splitting is performed.  In this case though, use `--`
      before the command so that options are passed to the command, rather than
      this script.

    Options:
        -m, --metrics-file PATH
        --memprof-file PATH
        --sample-interval FLOAT  Sampling period (in seconds), defaults to 0.1
        --help                   Show this message and exit.


sv_get_artifact_url
-----------------------------
Reads the ENV variable in a Gitlab CI job and constructs a URL for a given existing file or folder.

e.g.::

    sv_get_artefact_url output/test_file

will return :code:`${CI_PROJECT_URL}/-/jobs/${CI_JOB_ID}/artifacts/file/output/test_file`

while::

    sv_get_artefact_url output

will return :code:`${CI_PROJECT_URL}/-/jobs/${CI_JOB_ID}/artifacts/browse/output`

sv_get_target_branch
-----------------------------
Script to extract the target branch for a given project and commit hash.

Meant to be run within a Gitlab CI job and needs the following ENV variables defined:
 * CI_PROJECT_ID (automatic from CI job)
 * CI_COMMIT_SHA (automatic from CI job)
 * CI_API_TOKEN (to be set in the Gitlab project: settings -> pipelines -> add variable)

Related issue: https://gitlab.com/gitlab-org/gitlab-ce/issues/15280


sv_merge_json
-----------------------------
Merges dictionaries in <N>JSON files into one output file. Uses dict.update() |srarr| last occurrence of a key will take precedence.
Usage::

    sv_merge_json [OPTIONS] [INPUT_FILES]... OUTPUT


sv_remove_from_env
-----------------------------
Removes a path from an environment variable, e.g. ::

    sv_remove_from_env /a/b/c:/a/b/d:/d/b/a /a/b

will result in `/d/b/a`. Recommended use is to clean up ENV variables::

    PATH=`sv_remove_from_env /a/b/c:/a/b/d:/d/b/a /a/b`


sv_metric_diff
--------------------

::

    Usage: sv_metric_diff [OPTIONS] FILE_UNDER_TEST REFERENCE_FILE

      Display the difference between two metric (JSON) files.

      Examples:     sv_metric_diff
      skvalidate/data/examples/performance_metrics*.json     sv_metric_diff
      skvalidate/data/examples/file_metrics*.json

    Options:
      -o, --output-format [console|csv|markdown]
      --help                          Show this message and exit.


Example output:

::

    sv_metric_diff skvalidate/data/examples/file_metrics*
    +-----------------------------------------+------------+---------+-------------+--------+-----------+--------+
    | file                                    | metric     |   value |   ref value |   diff |   diff_pc | unit   |
    |-----------------------------------------+------------+---------+-------------+--------+-----------+--------|
    | continuous_integration_101.bin          | size_in_mb |    81   |        39.6 |   41.4 |  104.545  | MB     |
    | continuous_integration_101.root         | size_in_mb |    14.3 |         9.4 |    4.9 |   52.1277 | MB     |
    | continuous_integration_101_mctruth.root | size_in_mb |    90.3 |        31.9 |   58.4 |  183.072  | MB     |
    +-----------------------------------------+------------+---------+-------------+--------+-----------+--------+



sv_root_diff
--------------------
Calculates the difference between two ROOT (https://root.cern.ch/) files.
If a difference is present, the command will create plots for the distributions that differ.::

    sv_root_diff file_under_test reference_file --out-dir <path to output folder (for plots etc)>

Example output 1 - `test.a` only exists in the reference file:

.. image:: _static/root_diff/test.a.png
   :target: _static/root_diff/test.a.png

Example output 2 - `test.y` exists in both, but different random seed:

   .. image:: _static/root_diff/test.y.png
      :target: _static/root_diff/test.y.png


sv_version
------------

::

    sv_version 
    scikit-validate version: 0.3.7

    sv_version --plain
    0.3.7


run-clang-tidy
--------------
From https://github.com/llvm-mirror/clang-tools-extra/blob/master/clang-tidy/tool/run-clang-tidy.py

Runs clang-tidy in parallel for the code base::

    run-clang-tidy <path to code base>



.. |srarr|    unicode:: U+02192 .. RIGHTWARDS ARROW
