#!/usr/bin/env bash
export OUT_DIR=output/metrics
mkdir -p ${OUT_DIR}
# reference run
dd if=/dev/zero of=file1 bs=1048576 count=10
dd if=/dev/zero of=file2 bs=1048576 count=42

sv_file_info file1 file2 --metrics-file=${OUT_DIR}/file_metrics_ref.json

sv_execute \
  -m ${OUT_DIR}/performance_metrics.json \
  --memprof-file ${OUT_DIR}/stress_1.dat \
  -- \
  stress --cpu 1 --io 1 --vm 1 --vm-bytes 128M --timeout 10s --verbose

sv_execute \
    -m ${OUT_DIR}/performance_metrics.json \
    --memprof-file ${OUT_DIR}/stress_2.dat \
    -- \
    stress --cpu 1 --io 1 --vm 1 --vm-bytes 200M --timeout 15s --verbose

rm -f file1 file2
