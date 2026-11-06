# Configuration

Everything is in `config/config.yaml`, with a comment on each key, checked at
start-up against `workflow/schemas/config.schema.yaml`. An analysis workflow
importing this one as a module passes its own config, so these keys go in that
config too.

## 1. Point it at the delivery

`delivery_root` is the folder holding the delivery. It is a property of the
machine, so set it in a workflow profile, which Snakemake reads automatically:

```bash
mkdir -p profiles/default
cp profiles/default.example/config.yaml profiles/default/config.yaml
# edit:  delivery_root=/abs/path/to/the/delivery
```

`profiles/default/` is gitignored. The run refuses to start if
`delivery_root` does not exist.

## 2. Describe the delivery

| key | what to set |
|---|---|
| `universe` | the people file: id, sex (and its labels in `sex_values`), birth and death columns, date format |
| `sources.<name>` | one entry per diagnosis file: id, date, ICD code, date format; optionally `position` / `primary_position` (principal diagnosis), `episode_flags` (admission types to record, e.g. obstetric) and `icd9_changeover` |
| `sentinels`, `mid_month_day` | the delivery's codes for "unknown", and where month-precision dates land |
| `map_icd9` | map ICD-9 records to ICD-10 with the CMS GEM |
| `scale` | the CSV encoding and memory bounds; these never change a result |

Set `icd9_changeover` only for a file where the ICD-9 → ICD-10 changeover was
measured: before it, V/E-led codes are read as ICD-9.

## 3. What to ingest

| key | what it decides |
|---|---|
| `records.from` / `records.to` | records dated outside this window are not ingested |
| `buckets.n` / `buckets.seed` | optional: random person groups for a grouped bootstrap |

The test case in `.test/config/config.yaml` has the same keys, on the synthetic
delivery in `.test/data`.
