#!/usr/bin/env bash
# `scale` sets only how much is held in memory at once, so changing it must not
# change a single output byte. Runs the test case twice, once with the default
# batches and once with tiny ones, and compares results/out/.
set -euo pipefail
cd "$(dirname "$0")/.."

run() { snakemake --directory .test --workflow-profile none --sdm conda -c 4 \
          --resources mem_mb=8000 --show-failed-logs --forceall "$@"; }

ref=.test/results/out.default
rm -rf "$ref"
run
cp -r .test/results/out "$ref"
run --configfile .test/config/variants/small_batches.yaml

# A comparison over zero files would report "same".
n=$(find "$ref" -type f | wc -l)
[ "$n" -gt 0 ] || { echo "FAIL: the default run wrote nothing to results/out/"; exit 1; }
diff -r "$ref" .test/results/out
echo "PASS: $n files in results/out/ identical with tiny batches"
