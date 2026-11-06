"""The people file into the universe (bpskit.universe.build_universe)."""

import sys

# Everything printed, and any traceback, goes to the rule's log.
sys.stdout = sys.stderr = open(snakemake.log[0], "w", buffering=1)

from bpskit.transfer import write_ids
from bpskit.universe import build_universe

buckets = snakemake.params.buckets or {}  # optional: {n, seed}

universe, all_ids, summary = build_universe(
    snakemake.input.socio,
    snakemake.params.universe,
    snakemake.params.sentinels,
    snakemake.params.mid_month_day,
    n_buckets=buckets.get("n"),
    seed=buckets.get("seed", 1),
)
write_ids(all_ids, snakemake.output.ids)
universe.to_parquet(snakemake.output.universe, index=False)
summary.to_csv(snakemake.output.summary, index=False)
