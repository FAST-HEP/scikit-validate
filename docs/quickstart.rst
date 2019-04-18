Quickstart
==========


Storing resource usage
----------------------
Especially when constrained by available computing resources it is good to keep an eye on the resource usage of your \
analysis/application. For this purpose we provide the `sv_execute` command which encapsulates the script/executable \
and periodically checks the memory usage as well as reports the time taken at the end.

The following will execute ``stress --cpu 1 --io 1 --vm 1 --vm-bytes 128M --timeout 10s --verbose`` and output the \
resource usage into the ``resource_metrics.json`` file.

 .. code-block:: bash

    sv_execute -m resource_metrics.json \
       -- \
       stress --cpu 1 --io 1 --vm 1 --vm-bytes 128M --timeout 10s --verbose

In the first part, ``sv_execute -m resource_metrics.json``, we set the parameters for ``sv_execute``. ``--`` marks the \
end of ``sv_execute`` parameters, everthing after that is considered as the command (and parameters) to be executed.
The standard output of the called command is uneffected:

 .. code-block:: bash

    ...
    stress: dbug: [1844521] allocating 134217728 bytes ...
    stress: dbug: [1844521] touching bytes in strides of 4096 bytes ...
    ...
    >>> Ran command: "stress --cpu 1 --io 1 --vm 1 --vm-bytes 128M --timeout 10s --verbose"
    >>> in 11.424817s and used 93.3 MB of memory.



Storing file information
------------------------

Comparing two ROOT_ files
--------------------------


Adding high-level information
-----------------------------


 .. _ROOT: https://root.cern.ch/
