"""One diagnosis file into harmonised events (bpskit.ingest.ingest_source)."""

import sys

# Everything printed, and any traceback, goes to the rule's log.
sys.stdout = sys.stderr = open(snakemake.log[0], "w", buffering=1)

from bpskit.ingest import ingest_source

records = snakemake.params.records

ingest_source(
    snakemake.input.file,
    snakemake.input.universe,
    snakemake.params.source,
    name=snakemake.wildcards.source,
    sentinels=snakemake.params.sentinels,
    mid_month_day=snakemake.params.mid_month_day,
    map_icd9=snakemake.params.map_icd9,
    washout_from=records["from"],
    last_date=records["to"],
    scale=snakemake.params.scale,
    events_out=snakemake.output.events,
    episodes_out=snakemake.output.episodes,
    qc_out=snakemake.output.qc,
    ids_out=snakemake.output.ids,
)
