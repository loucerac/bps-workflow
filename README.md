# bps-workflow

The shared first step of every Snakemake workflow on a BPS (Base Poblacional de
Salud, Servicio Andaluz de Salud) delivery. It reads the delivery into a
universe and dated, ICD-10-harmonised events, reports their quality, and
checks that nothing leaving the data machine names a patient.

**Start here if you are new to the BPS workflows.** This workflow is small,
runs on its own in under a minute on synthetic data, and everything the
analysis workflows do builds on its outputs:

- [bps-sex-differences-workflow](https://github.com/loucerac/bps-sex-differences-workflow):
  sex differences in recorded incidence, by diagnostic origin;
- [bps-disease-trajectories-workflow](https://github.com/loucerac/bps-disease-trajectories-workflow):
  directional diagnosis pairs and disease trajectories.

The code each rule calls lives in the [bpskit](https://pypi.org/project/bpskit/)
Python package; this repository holds the rules.

## Run it

You need Linux x86-64 and [pixi](https://pixi.sh), which installs Snakemake,
conda and the linters:

```bash
curl -fsSL https://pixi.sh/install.sh | sh && exec $SHELL   # once per user, no root
pixi install --locked
pixi run test-workflow    # every rule on the synthetic delivery in .test/data
```

`.test/config/variants/` holds config overlays for the optional branches
(`pixi run test-workflow --configfile .test/config/variants/buckets.yaml`), and
`pixi run test-batches` checks that the batch sizes in `scale` change no output
byte. CI runs each of them.

The first run builds the rule environment (`workflow/envs/bpskit.yaml`) with
conda, which takes a few minutes. Everything goes to `.test/results/`:

```
results/work/universe.parquet              one row per person: idx, sex, birth, death (+ bucket)
results/work/events/<source>.parquet       idx, day, ICD-10 code (+ is_primary), from washout on
results/work/events/<source>.episodes.parquet   (idx, day, flag) of flagged admissions
results/work/ids/*.parquet                 every patient id read, for the transfer check
results/out/tables/universe_summary.csv    persons and deaths by sex and birth decade
results/out/tables/quality/harmonisation.csv   records per year by coding system (ICD-9 mapped or not)
results/out/tables/quality/plausibility.csv    records that cannot be true for their person
results/out/run/pullable_check.txt         PASS, or what refused
```

`results/work/` holds per-person data and never leaves the data machine.
`results/out/` holds aggregates. `check_outputs` passes it only if no file
contains a patient id or a per-person column (bpskit's transfer check).

## The four rules

| rule | reads | writes |
|---|---|---|
| `universe` | the people file | the universe; every delivered id, written *before* persons with unknown sex or birth are dropped |
| `ingest_source` | one diagnosis file (one job per source) | its events, with ICD-9 mapped to ICD-10; episode flags; a harmonisation table; ids not in the universe |
| `quality` | the events | the harmonisation and plausibility tables |
| `check_outputs` | everything in `results/out/` | the transfer verdict |

After `universe`, per-person files carry `idx` (the person's row in the
universe), never the patient id.

## Use it in an analysis workflow

Import it as a Snakemake module, pinned to a release:

<!-- x-release-please-start-version -->
```python
configfile: "config/config.yaml"   # holds this workflow's keys too (config/README.md)


module bps:
    snakefile:
        github("loucerac/bps-workflow", path="workflow/Snakefile", tag="v0.1.1")
    config:
        config


use rule universe from bps


use rule ingest_source from bps


use rule quality from bps


# The transfer check must run after the analysis's own outputs.
use rule check_outputs from bps with:
    input:
        FINAL_OUTPUTS,
        ids=expand("results/work/ids/{name}.parquet", name=["universe", *config["sources"]]),
```
<!-- x-release-please-end -->

The analysis's rules then read `results/work/universe.parquet` and
`results/work/events/<source>.parquet`.

## Configure it for a delivery

See [config/README.md](config/README.md).

## Releases

Commit messages are [conventional commits](https://www.conventionalcommits.org)
(`feat:`, `fix:`, `chore:`, ...). On every push to `main`, release-please keeps a
release PR open with the next version and its `CHANGELOG.md` entry: `fix:` bumps
the patch, `feat:` the minor version. Merging it tags `vX.Y.Z`; an analysis
workflow then moves its `tag=` to the new release.
