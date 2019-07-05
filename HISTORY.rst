Changelog
=========


0.3.1
------------
- Sv_root_info: fixed mask for non-readable. [kreczko]
- Tagged version 0.3.0. [kreczko]
- Merge pull request #12 from kreczko/kreczko-root-info. [Luke Kreczko]

  Added sv_root_info for inspection of ROOT files with uproot
- Sv_root_info: fixed lint errors. [kreczko]
- Sv_root_info: added read test for non-obvious branches. [kreczko]
- Added sv_root_info for inspection of ROOT files with uproot. [kreczko]
- Tagged version 0.2.24. [kreczko]
- When getting pipeline jobs: filter for only the last iteration of a
  particular job. [kreczko]
- Tagged version 0.2.23. [kreczko]
- Fix git.create_patch behaviour for empty diffs. [kreczko]
- Tagged version 0.2.22. [kreczko]
- Cpp_check_format: added "--exclude" parameter. [kreczko]
- Cpp_check_format: fixed patch file (missing new line at the EOF)
  [kreczko]
- Tagged version 0.2.21. [kreczko]
- Tagged version 0.2.20. [kreczko]
- Added ability to overwrite default cpp_check_format template.
  [kreczko]
- Cpp_check_format report: separated path & command variables. [kreczko]
- Tagged version 0.2.19. [kreczko]
- Sv_cpp_check_format: fixed return code. [kreczko]
- Tagged version 0.2.18. [kreczko]
- Sv_cpp_check_format: fixes issues with instructions. [kreczko]
- Tagged version 0.2.17. [kreczko]
- Increased version to 0.2.17. [kreczko]
- Sv_cpp_check_format: fixes issues with detached head. [kreczko]
- Merge pull request #11 from kreczko/kreczko-cpp_format. [Luke Kreczko]

  New CI check: sv_cpp_check_format
- Increased version to 0.2.16. [kreczko]
- Added wrappers for git commands. [kreczko]
- Sv_cpp_check_format: added report creation & publishing. [kreczko]
- Sv_cpp_check_format: added file retrival, formatting and patch
  creation. [Luke Kreczko]
- Added draft for cpp_check_format. [kreczko]
- Tagged version 0.2.15. [kreczko]
- Collapsible details for detailed validation report (issue #8)
  [kreczko]
- Extending gitignore for test files. [kreczko]
- Updated history & changelog. [kreczko]
- Fixed HISTORY formatting. [kreczko]
- Fixed release example in README. [kreczko]
- CI: updated user & password for travis-ci.com. [kreczko]
- Tagged version 0.2.14. [kreczko]
- Tagged version 0.2.14. [kreczko]
- Tagged version 0.2.14. [kreczko]
- Merge pull request #9 from kreczko/kreczko-issue-8. [Luke Kreczko]

  Collapsible details for validation report (issue #8)
- CI: more verbose install. [kreczko]
- CI: updating Ubuntu distribution from 14.04 to 16.04. [kreczko]
- CI: added demo report. [kreczko]
- CI: added "make install" to script. [kreczko]
- CI: installing packages needed for development. [kreczko]
- Collapsible details for validation report (issue #8) [kreczko]
- Fix travis config. [kreczko]
- Updated travis condition for deployment. [kreczko]
- Merge pull request #7 from kreczko/kreczko-travis. [Luke Kreczko]

  Updating travis to follow Gitlab CI
- Added Gitter link to README. [kreczko]
- README: added URL to issues. [kreczko]
- Updated travis to follow .gitlab-ci.yml. [kreczko]


0.2.13 (2019-05-13)
-------------------
- Merge branch 'kreczko-reduce-timeouts' into 'master' [Lukasz Kreczko]

  Reduce timeouts during artifact download

  See merge request fast-hep/public/scikit-validate!14
- Version 0.2.12 --> 0.2.13. [kreczko]
- Added timeout to job artifact download. [kreczko]
- Merge branch 'kreczko-docs' into 'master' [Lukasz Kreczko]

  Documentation "day" summary

  See merge request fast-hep/public/scikit-validate!13
- Docs: expanded README and added quickstart draft. [kreczko]
- Docs: added custom CSS. [kreczko]
- Docs: switched from alabaster to sphinx_rtd_theme. [kreczko]
- Docs: added logo. [kreczko]
- Fixed flake8. [kreczko]
- Docs: added sphinxcontrib-apidoc extension. [kreczko]
- Fixed Sphinx documentation warnings. [kreczko]
- README: Fixed badges and bullet list indents. [kreczko]
- Docs: fixed typo to GitLab repo. [kreczko]
- Merge branch 'kreczko-better-error-messages' into 'master' [Lukasz
  Kreczko]

  Improvements to reporting: error messages & quality of life

  Closes #6

  See merge request fast-hep/public/scikit-validate!12
- Fixed issue #6: Bug: gitlab.get_pipeline_job returns first job only.
  [kreczko]
- Version 0.2.11 --> 0.2.12. [kreczko]
- Download_validation_outputs: do not append validation job name if
  already part of path (e.g. user defined) [kreczko]
- Version 0.2.10 --> 0.2.11. [kreczko]
- Validation report: batch size and line breaks are now configurable.
  [kreczko]
- Gitlab.download_artifact will skip download if output file exists.
  [kreczko]
- Report: added debug information for validation report. [kreczko]
- Version 0.2.9 --> 0.2.10. [kreczko]
- Report: moved parsing errors their respective subsections. [kreczko]
- Merge branch 'kreczko-report-tuning' into 'master' [Lukasz Kreczko]

  Fine-tuning reporting

  Closes #5

  See merge request fast-hep/public/scikit-validate!11
- Report: allow file download to fail (e.g. failed jobs in pipeline)
  [kreczko]
- Validation report: increased the number of images per row from 5 to 8.
  [kreczko]
- Validation report: simplified image loading. [kreczko]
- Gitlab artifact url: normalize path before use to exclude ".."
  [kreczko]
- Validation report: added tests for _get_links_for_reports. [kreczko]
- Test_gitlab: added path_type to URL test. [kreczko]
- Validation report: separate report creation from link creation.
  [kreczko]
- Validation report: add links to original images. [kreczko]
- Validation report: switched details from HTML to PDF output. [kreczko]
- Validation report: remove unused loop variable. [kreczko]
- Validation report: reduced image size & added overview. [kreczko]
- Sv_root_diff: fixed incorrect function name for processing. [kreczko]
- Version 0.2.8 --> 0.2.9. [kreczko]
- Sv_root_diff: added multi-processing support. [kreczko]
- Sv_root_diff: added reason for UNKNOWN status. [kreczko]
- Vis.draw_diff: trying to make plotting thread-safe. [kreczko]
- Sv_root_diff: added progressbar. [kreczko]
- Sv_root_diff: parallelised using threads. [kreczko]
- Added new command: sv_absolute_to_relative_path. [kreczko]
- Sv_execute: units are a separate entry --> shorten metric names.
  [kreczko]
- Gitlab: always take local file path as relative to project path for
  URLs. [kreczko]
- Version 0.2.7 --> 0.2.8. [kreczko]
- Sv_make_report: fixed memeory_profile output file names for commands
  that include paths. [kreczko]
- Version 0.2.6 --> 0.2.7. [kreczko]
- Sv_root_diff: fix _reset_infinities for empty values. [kreczko]
- Version 0.2.5 --> 0.2.6. [kreczko]
- Merge branch 'kreczko-root-diff-tuning' into 'master' [Lukasz Kreczko]

  Bug fixes & generalisation for sv_root_diff

  See merge request fast-hep/public/scikit-validate!10
- Vis.find_limits: fixed behaviour for empty arrays. [kreczko]
- Added unpack np array function to serialize JSON. [kreczko]
- Sv_root_diff: fixed issue with comparison between empty entries.
  [kreczko]
- Sv_root_diff: added more information for WARNING & FAILED statuses.
  [kreczko]
- Compare: added maxRelativeDifference and generalized is_ok function.
  [kreczko]
- Sv_root_diff: switch WARNING color from invalid "orange" to valid
  "Orange3" [kreczko]
- Sv_root_diff: improve robustness for 2D arrays and arrays of strings.
  [kreczko]
- Version 0.2.4 --> 0.2.5. [kreczko]
- Sv_execute: replace _thread with six.moves._thread. [kreczko]
- Sv_execute: replaced thread with six._thread. [kreczko]
- CI: increased sleep time for report stage. [kreczko]
- Sv_execute: memory profile monitoring now in separate thread.
  [kreczko]
- Added software module to setup.py. [kreczko]
- Version 0.2.2 --> 0.2.3. [kreczko]
- Added gitlab.get_pipeline_url. [kreczko]
- Version 0.2.1 --> 0.2.2. [kreczko]
- Merge branch 'kreczko-memory-profile' into 'master' [Lukasz Kreczko]

  Adding memory profiles to validation report

  See merge request fast-hep/public/scikit-validate!9
- CI: added delay of 60 seconds to report stage. [kreczko]
- CI: added PNG files to artifacts for report stage. [kreczko]
- Performance report: switched from raw link to dressed link for
  profiling image. [kreczko]
- Updated example root_diff files with new plotting style and command
  (root_diff -> sv_root_diff) [kreczko]
- Moved plotting style definitions from vis.profile to vis. [kreczko]
- CI report: fixed typo in report configuration. [kreczko]
- CI: fixed URL for reference memory profile. [kreczko]
- Gitlab: fix relative import for Python 2.7. [kreczko]
- Gitlab.DiskStreamer: create dowload directory if it does not exist.
  [kreczko]
- Gitlab.get_jobs_for_stages: fixed typo in debug message. [kreczko]
- Report: memory profile now return full URL (local or CI) [kreczko]
- Fixed download_from_gitlab. [kreczko]
- CI: source instead of execute. [kreczko]
- Fixed lint errors. [kreczko]
- Implemented vis.draw_profile. [kreczko]
- Fix newlines when reading & writing the memory_profile. [kreczko]
- Fixed profile dictionary for profile template. [kreczko]
- Remaned example memory profile files. [kreczko]
- Added memory_profile to demo report. [kreczko]
- Fixed paths for memory profile files in CI report. [kreczko]
- Raised min. version for memory_profiler to 0.54 (first with mprof
  module) [kreczko]
- Added memory profile data examples. [Lukasz Kreczko]
- Added vis.profile. [Lukasz Kreczko]
- Report: changed import of vis module, draw_profiles -->
  vis.draw_profiles. [Lukasz Kreczko]
- Added profile to CI report. [Lukasz Kreczko]
- Added processing of profile files to report. [Lukasz Kreczko]
- Added processing for memory profile timestamps. [Lukasz Kreczko]
- Added function to split memory_profiler output from multiple commands.
  [Lukasz Kreczko]
- Using a single profile file for memory_profile. [Lukasz Kreczko]
- Switched memory_profile from just the exe to the full command (as done
  for the metrics) [Lukasz Kreczko]
- Added downloaded files to report artifacts. [Lukasz Kreczko]
- Downloading performace JSON and memory profiles for performance
  report. [Lukasz Kreczko]
- Added special keyword "download" to report sections. [Lukasz Kreczko]
- Added documentation draft for report config. [Lukasz Kreczko]
- Added download capability to io package. [Lukasz Kreczko]
- Added gitlab.get_pipeline_job. [Lukasz Kreczko]
- Split performance validation across two jobs. [Lukasz Kreczko]
- Added memory profile to CI. [Lukasz Kreczko]
- Added memory profile to sv_exectute. [Lukasz Kreczko]
- Added memory_profiler as dependency. [Lukasz Kreczko]
- Merge branch 'BK_allow_multiple_argument_cmds' into 'master' [Lukasz
  Kreczko]

  Add support for mutiple positional arguments being used as the command to run

  See merge request fast-hep/public/scikit-validate!8
- Use new command-line style in ci. [Ben Krikler]
- Remove TODO comment that I'd added. [Ben Krikler]
- Add support for mutiple positional arguments being used as the command
  to run + pep8. [Ben Krikler]


0.2.1 (2019-03-12)
------------------
- Version 0.2.0 --> 0.2.1. [Lukasz Kreczko]
- Merge branch 'kreczko-rename-commands' into 'master' [Lukasz Kreczko]

  More user-friendly command names

  See merge request fast-hep/public/scikit-validate!7
- Switch to new command names in the CI. [Lukasz Kreczko]
- Updated command names & added TODOs. [Lukasz Kreczko]
- All commands now start with "sv\_" [Lukasz Kreczko]
- Version 0.2.0. [kreczko]
- Merge branch 'kreczko-better-validation-report' into 'master' [Lukasz
  Kreczko]

  Added better validation report

  See merge request fast-hep/public/scikit-validate!6
- New command: submit_report_to_mr to add reports to the MR. [kreczko]
- Fix update of existing note in MR for report. [kreczko]
- Fix overwritting of values for detailed report. [Lukasz Kreczko]
- Fix validation detail template & remove debugging. [Lukasz Kreczko]
- Fix missing summary report. [Lukasz Kreczko]
- Made updating merge request with report available for GitLab < 11.6.
  [Lukasz Kreczko]
- Fixed job_name. [Lukasz Kreczko]
- Added reporting to parent merge request. [Lukasz Kreczko]
- Added io.resolve_wildcard_path. [Lukasz Kreczko]
- Added job_name variable to detailed validation report. [Lukasz
  Kreczko]
- Fixed report.format_software_versions. [Lukasz Kreczko]
- Added tests for report.format_software_versions. [Lukasz Kreczko]
- Reraising exception for template rendering. [Lukasz Kreczko]
- Added logging. [Lukasz Kreczko]
- Remove automatic reporting for now. [Lukasz Kreczko]
- Added debugging for validation detail template. [Lukasz Kreczko]
- Added HTML and PDF output formats for validation report. [Lukasz
  Kreczko]
- Replacing pdfkit with xhtml2pdf. [Lukasz Kreczko]
- Added PDF output for validation HTML. [Lukasz Kreczko]
- Added pdfkit dependency. [Lukasz Kreczko]
- Added reporting to merge request. [Lukasz Kreczko]
- Added documentation for validation report. [Lukasz Kreczko]
- Replaced image & validation_detail URLs with RAW urls. [Lukasz
  Kreczko]
- Downloading relevnt validation artifacts. [Lukasz Kreczko]
- Added download to disk option for gitlab.download_artifact. [Lukasz
  Kreczko]
- Added ls for report job (debugging) [Lukasz Kreczko]
- Resolve image paths for validation jobs. [Lukasz Kreczko]
- Added validation reports to CI artifacts. [Lukasz Kreczko]
- Extract distributions from validation_json before passing them on.
  [kreczko]
- Fixed prefix path for output_path in root_diff. [kreczko]
- Added missing output JSON for validate-root-diff-1_3. [kreczko]
- Fixed incorrect function calls. [kreczko]
- Added job_filter to GitLab job retrieval. [kreczko]
- Added validation report to CI. [kreczko]
- Switched Demo report to use more general values. [kreczko]
- Added more performance metrics. [kreczko]
- Added detailed validation report. [kreczko]
- Replaced demo report validation with new summary. [kreczko]
- Added validation summary. [kreczko]
- Added error reporting in validation template. [kreczko]
- Root_diff: added output_path to JSON output. [kreczko]
- Fixed tests for compare_two_root_files. [kreczko]
- Fixed lint issues. [kreczko]
- CI: fixed dependency for report. [kreczko]
- Added draft for validation detail. [Lukasz Kreczko]
- Tidied up symbols for demo report. [Lukasz Kreczko]
- Added 3rd validation example. [Lukasz Kreczko]
- Added examples for root_diff. [Lukasz Kreczko]
- Generalised gitlab download of JSON data. [Lukasz Kreczko]
- Added prefix to root_diff. [Lukasz Kreczko]
- Split root_diff validation job into two jobs (1 for each comparison)
  [Lukasz Kreczko]
- Added root_diff summary. [Lukasz Kreczko]
- Making all produced JSON files human-readable. [Lukasz Kreczko]
- Added proper reporting to root_diff. [Lukasz Kreczko]
- Moved reseting infinities from draw_diff to root_diff. [Lukasz
  Kreczko]
- Added short-hand option for root_diff:out-dir. [Lukasz Kreczko]
- Added first version of the logo. [kreczko]
- Merge branch 'kreczko-gitlab-access' into 'master' [Lukasz Kreczko]

  First functional draft for pipeline reports

  See merge request fast-hep/public/scikit-validate!5
- Fixed web_url_raw in gitlab.get_jobs_for_stages. [kreczko]
- Added skvalidate.report.get_jobs_for_stages. [kreczko]
- Moved report.demo._format_status to report.format_status. [kreczko]
- Ok -> success, fail -> failed to be more consistent with gitlab.
  [kreczko]
- Link -> web_url to be more consistent with gitlab. [kreczko]
- Allow for artifact download to fail. [kreczko]
- Fixed prefix for detect_software_versions in CI. [kreczko]
- Made software_version retrieval more resilient against missing data.
  [kreczko]
- Fix streamer for bytestrings. [kreczko]
- Returning to previous version but with additional error-handling.
  [kreczko]
- Updated python-gitlab to latest master to avoid workaround. [kreczko]
- Made install procedure a bit more quiet. [kreczko]
- Added workaround for python-gitlab bug. [kreczko]
- Make installation of dependencies & after_script silent. [kreczko]
- Report: print section properties on error. [kreczko]
- Added robustness to performance report: only format as number if
  variable is a number. [kreczko]
- Added quiet option for detect_software_versions. [kreczko]
- Enable streaming for gitlab job artifact retrieval. [kreczko]
- Replaced CI_ATUH_TOKEN with read-only API token from bot-account.
  [kreczko]
- Fixed name for software_versions.json in CI. [kreczko]
- Added gitlab package. [kreczko]
- Fixed detect_software_versions after_script. [kreczko]
- Fixed unused module in get_artifact_url command. [kreczko]
- Added reporting to current CI. [kreczko]
- Added gitlab connectors. [kreczko]
- Restricting gitlab dependency to be >=1.7.0. [kreczko]
- Moved logic from get_artifact_url command to skvalidate.gitlab.
  [kreczko]
- Re-enabled status symbols. [kreczko]
- Updated gitlab report config with pipelines and latest validation
  section. [kreczko]
- Added prefixes to scan_software_version to allow for multiple
  environments names. [kreczko]
- Removed obsolete function in report. [kreczko]
- Added validation info from JSON. [kreczko]
- Fixed table in pipeline template. [kreczko]
- Fixed lint in .software. [kreczko]
- Io: made save_metrics_to_file more general. Now have
  update_data_in_json,write_data_to_json & read_data_from_json.
  [kreczko]
- Added new pipelines to demo report. [kreczko]
- Added lower_is_better value to metrics. [kreczko]
- Added output file for detect_software_versions. [kreczko]
- Added detect_software_versions command. [kreczko]
- Replaced build, test and software sections in report with pipeline
  section. [kreczko]
- Added markdown2 as new dependency. [kreczko]
- Fixed commands and metric names for performace and file report.
  [kreczko]
- Added "make_report" command. [kreczko]
- Removed obsolete print statement. [kreczko]
- Added plumbum as new depedency. [kreczko]
- Merge branch 'kreczko-update-metrics' into 'master' [Lukasz Kreczko]

  Fixed printouts for add_file_metrics & execute_with_metrics

  See merge request fast-hep/public/scikit-validate!4
- Fixed tests for new-style metrics. [kreczko]
- Moved report.demo.get_metrics -> report.get_metrics. [kreczko]
- Fixed printouts for add_file_metrics & execute_with_metrics. [kreczko]
- Merge branch 'kreczko-update-metrics' into 'master' [Lukasz Kreczko]

  Updated metrics for add_file_metric & execute_with_metrics to new-style metrics

  See merge request fast-hep/public/scikit-validate!3
- Fixed name of performance metrics in CI. [kreczko]
- Added validation of the metrics pipeline (run & file metrics ->
  report) to the CI. [kreczko]
- Updated execute_with_metrics to produce new-style metrics. [kreczko]
- Updated file metrics to new style. [kreczko]
- Merge branch 'kreczko-backwards-compatible-metrics' into 'master'
  [Lukasz Kreczko]

  Added backwards compatible metrics

  See merge request fast-hep/public/scikit-validate!2
- Fixed linter issues. [kreczko]
- Converting metrics from old to new by default. [kreczko]
- Added method to convert from old to new metrics. [kreczko]
- Moved skvalidate.compare.compare_metrics to
  skvalidate.compare.metrics.compare_metrics. [kreczko]
- Fixed typo in compare_metrics. [kreczko]
- Merge branch 'kreczko-report' into 'master' [Lukasz Kreczko]

  Added report creation functionality

  See merge request fast-hep/public/scikit-validate!1
- Moved data to skvalidate/data. [kreczko]
- Added report package. [kreczko]
- Trying indirect call to make_demo_report in CI. [kreczko]
- Changed version: 0.1.8 --> 0.2.0rc1. [kreczko]
- Run demo report under python 3.7. [kreczko]
- Added Jinja2 to dependencies. [kreczko]
- Added demo_report to validation stage. [kreczko]
- Fixed potential Python2 syntax problems. [Lukasz Kreczko]
- Added PyYAML as a dependency. [Lukasz Kreczko]
- Fixed lint errors. [Lukasz Kreczko]
- Make report: output file now as command line argument instead of
  config. [Lukasz Kreczko]
- Added metric comparison functionality. [Lukasz Kreczko]
- Fixed metric templates (files & performance) [Lukasz Kreczko]
- Added metric examples. [Lukasz Kreczko]
- Made tests more verbose. [Lukasz Kreczko]
- Updated gitlab report config & name. [Lukasz Kreczko]
- Updated template paths in demo report config. [Lukasz Kreczko]
- Moved config into data folder. [Lukasz Kreczko]
- Added draft for reporting. [Lukasz Kreczko]
- Added status symbols to demo. [Lukasz Kreczko]
- Moved templates to data folder. [Lukasz Kreczko]
- Made default templates more resilient. [Lukasz Kreczko]
- Added default report templates. [Lukasz Kreczko]
- Added example report configs. [Lukasz Kreczko]
- Improved development install. [Lukasz Kreczko]
- Version 0.1.7 --> 0.1.8. [kreczko]
- Add_file_metrics: added fix for Python3 & test. [kreczko]
- Version 0.1.6 --> 0.1.7. [kreczko]
- Execute_with_metrics: added fix for Python3 & test. [kreczko]
- Version 0.1.5 --> 0.1.6. [kreczko]
- Made run-clang-tidy Python3 compatible. [kreczko]
- Fixed pep8 error in vis. [kreczko]
- Version 0.1.4 --> 0.1.5. [kreczko]
- Disabled log scale for diff plot. [kreczko]
- Setting minY to non-zero for logarithmic plots. [kreczko]
- Disabled logY setting if negative values are found. [kreczko]
- V0.1.3 --> v0.1.4. [kreczko]
- Execute_with_metrics: added soft-fail to IOException on writing
  metrics file. [kreczko]
- Added tests for get_target_branch. [kreczko]
- Fix missing import. [kreczko]
- Version 0.1.2 --> 0.1.3. [kreczko]
- Improved error-handling for get_target_branch and added target &
  default branches. [kreczko]
- Worked through the stricter pep8 set. [Lukasz Kreczko]
- Added default target_branch to get_target_branch. [Lukasz Kreczko]
- Version 0.1.1 --> 0.1.2. [kreczko]
- Visualisation adjustments for root_diff. [kreczko]
- Fixed python3 issues with io._walk. [kreczko]
- Version 0.1.0 --> 0.1.1. [kreczko]
- Replaced io._walk with a more robust equivalent. [kreczko]
- Added automated logy & x-limits to drawing. [kreczko]
- Added code to generate tests/samples/objects.root. [kreczko]
- Steeled diff calculation, fixed normalisation (now w.r.t. reference)
  and reporting non-comparible branches in root_diff. [kreczko]
- Made io.unpack more robust to str-arrays. [kreczko]
- Fixed pep8 error: unused include in test_io. [kreczko]
- Fixed "make test" [kreczko]
- Version 0.0.7 --> 0.1.0. [kreczko]
- Added comparison of object data to tests. [kreczko]
- Updated io.walk to handle & unpack objects. [kreczko]
- Version 0.0.6 -> 0.0.7. [kreczko]
- Automatically expose commands directly to command line. [kreczko]
- Made sure vector branches are flattened before comparison. [kreczko]
- Updated tests for vector branch. [kreczko]
- Added vector variable to test samples. [kreczko]
- Tagged version 0.0.6. [kreczko]
- Added image examples for root_diff. [kreczko]
- Tagged version 0.0.5. [kreczko]
- Added KS test to drawing. [kreczko]
- Moved compare_two_root_files to compare.compare_two_root_files.
  [kreczko]
- Fixed "a" branch in tests/samples/test_3.root. [kreczko]
- Creating output/validate/test_1_3 in CI. [kreczko]
- Removed print from io test. [kreczko]
- Fixed pep8 errors. [kreczko]
- Parametrised IO tests. [kreczko]
- Switched "make test" from py.test to pytest. [kreczko]
- Fixed test samples. [kreczko]
- Added compare and vis packages to setup.py. [kreczko]
- Moved draw_diff to vis.draw_diff. [kreczko]
- _compare_mctruth --> _compare. [kreczko]
- Moved _diff and _isOK to compare.difference & compare.is_ok. [kreczko]
- Moved store_diff to io.save_array_to_file. [kreczko]
- Moved walk function into skvalidate.io. [kreczko]
- Added folder creation to validation step. [kreczko]
- Added installation to validation step in CI. [kreczko]
- Added six to substitute xrange. [kreczko]
- Fixed pep8. [kreczko]
- Added validation step to CI. [kreczko]
- Added test samples & generation script. [kreczko]
- Added auto-generated docs. [kreczko]
- Fix package description and align versions in __init__.py and
  setup.cfg. [kreczko]
- Fixed pep8 errors. [kreczko]
- Added get_artifact_url. [kreczko]
- Added folder for static docs content. [kreczko]
- Added root_diff draft. [kreczko]
- Added remove_from_env command. [kreczko]
- Updated documentation for all commands. [kreczko]
- Fixed indentation in README. [kreczko]
- Expanded on the features of scikit-validate. [Lukasz Kreczko]
- Renaming CLI class. [Lukasz Kreczko]
- Rename to scikit-validate. [Lukasz Kreczko]
- Added missing variable to setup.py. [kreczko]
- Version 0.0.2 --> 0.0.3. [kreczko]
- Added version lookup in setup.py from lz_validation. [kreczko]
- CI: simplyfied twine upload to pypi. [kreczko]
- Fixed behaviour of get_target_branch for non-MR branches. [kreczko]
- Added explitcit user and pw parameters for twine (upload_to_pypi.sh)
  [kreczko]
- Fixed comment in upload_to_pypi.sh. [kreczko]
- Fixed package distribution (was missing commands and io modules)
  [kreczko]
- Moved pypi upload into separate script. [kreczko]
- Fixed pypi deployment procedure. [kreczko]
- Fix gitlab-ci.yml. [kreczko]
- Added pypi upload. [kreczko]
- Updated failing test. [kreczko]
- Fixed linter errors. [kreczko]
- Moved linting to quick-checks stage. [kreczko]
- Added artifacts for build stage. [kreczko]
- Added gitlab-ci.yml. [kreczko]
- Added more tox setups. [kreczko]
- Added add_file_metrics command. [kreczko]
- Added general save_metrics_to_file to lz_validation.io. [kreczko]
- Added command to merge JSON files. [kreczko]
- Added script to run clang-tidy. [kreczko]
- Added execute_with_metrics command. [kreczko]
- Added command structure and get_target_branch command. [kreczko]
- Initial commit. [kreczko]


