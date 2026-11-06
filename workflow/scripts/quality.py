"""The harmonisation and implausible-record tables (bpskit.quality)."""

import sys

# Everything printed, and any traceback, goes to the rule's log.
sys.stdout = sys.stderr = open(snakemake.log[0], "w", buffering=1)

from bpskit.quality import harmonisation, plausibility

# {source name: events parquet}, from ingest_source.
events = dict(zip(snakemake.params.sources, snakemake.input.events))

harmonisation(snakemake.input.qc).to_csv(snakemake.output.harmonisation, index=False)
plausibility(snakemake.input.universe, events, snakemake.params.batch_rows).to_csv(
    snakemake.output.plausibility, index=False
)
