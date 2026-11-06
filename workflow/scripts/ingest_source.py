"""One diagnosis file into harmonised events (bpskit.ingest.ingest_source)."""

import sys

from bpskit.ingest import ingest_source

# Everything printed, and any traceback, goes to the rule's log.
sys.stdout = sys.stderr = open(snakemake.log[0], "w", buffering=1)  # noqa: SIM115
P, out = snakemake.params, snakemake.output
ingest_source(
    snakemake.input.file,
    snakemake.input.universe,
    P.source,
    name=snakemake.wildcards.source,
    sentinels=P.sentinels,
    mid_month_day=P.mid_month_day,
    map_icd9=P.map_icd9,
    washout_from=P.records["from"],
    last_date=P.records["to"],
    scale=P.scale,
    events_out=out.events,
    episodes_out=out.episodes,
    qc_out=out.qc,
    ids_out=out.ids,
)
