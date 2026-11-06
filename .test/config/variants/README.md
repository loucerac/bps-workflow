# Test variants

Each file here is laid over `.test/config/config.yaml` with `--configfile`, so it
holds only the keys it changes. CI runs one job per variant; locally:

    pixi run test-workflow --configfile .test/config/variants/<name>.yaml

| variant | what it exercises |
|---|---|
| `buckets.yaml` | bootstrap buckets on the universe (the base config has none) |
| `small_batches.yaml` | tiny read and write batches; `pixi run test-batches` checks that `results/out/` is byte-identical to the default run |

There is no `map_icd9: false` variant: the synthetic delivery holds no ICD-9
codes, so it would produce the default outputs and test nothing. bpskit's unit
tests (`tests/test_icd.py`, `tests/test_ingest.py`) cover the mapping.
