#!/usr/bin/env bash

# reference run
dd if=/dev/zero of=file1 bs=1048576 count=10
dd if=/dev/zero of=file2 bs=1048576 count=42
add_file_metrics file1 file2 --metrics-file=file_metrics_ref.json

execute_with_metrics \
  'stress --cpu 1 --io 1 --vm 1 --vm-bytes 128M --timeout 10s --verbose' \
  -m performance_metrics_ref.json

rm -f file1 file2

# validation run
dd if=/dev/zero of=file1 bs=1048576 count=12
dd if=/dev/zero of=file2 bs=1048576 count=20
add_file_metrics file1 file2 --metrics-file=file_metrics.json

execute_with_metrics \
  'stress --cpu 1 --io 1 --vm 1 --vm-bytes 200M --timeout 15s --verbose' \
  -m performance_metrics.json

rm -f file1 file2

# prepare report
cp -vp *metrics*.json skvalidate/data/examples/.
