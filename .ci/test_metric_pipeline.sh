#!/usr/bin/env bash

# reference run
dd if=/dev/zero of=file1 bs=1048576 count=10
dd if=/dev/zero of=file2 bs=1048576 count=42
sv_file_info file1 file2 --metrics-file=file_metrics_ref.json

sv_execute -m performance_metrics_ref.json -- \
  stress --cpu 1 --io 1 --vm 1 --vm-bytes 128M --timeout 10s --verbose

sv_execute -m performance_metrics_ref.json -- \
    stress --cpu 1 --io 1 --vm 1 --vm-bytes 200M --timeout 15s --verbose

rm -f file1 file2

# validation run
dd if=/dev/zero of=file1 bs=1048576 count=12
dd if=/dev/zero of=file2 bs=1048576 count=20
sv_file_info file1 file2 --metrics-file=file_metrics.json

sv_execute -m performance_metrics.json -- \
  stress --cpu 1 --io 1 --vm 1 --vm-bytes 128M --timeout 10s --verbose

sv_execute -m performance_metrics.json -- \
    stress --cpu 1 --io 1 --vm 1 --vm-bytes 200M --timeout 15s --verbose

rm -f file1 file2

# prepare report
cp -vp *metrics*.json skvalidate/data/examples/.
