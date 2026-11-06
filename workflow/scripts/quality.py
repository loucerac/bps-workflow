"""The harmonisation and implausible-record tables (bpskit.quality)."""

import sys

from bpskit.quality import harmonisation, plausibility

# Everything printed, and any traceback, goes to the rule's log.
sys.stdout = sys.stderr = open(snakemake.log[0], "w", buffering=1)  # noqa: SIM115
P, i, o = snakemake.params, snakemake.input, snakemake.output
harmonisation(i.qc).to_csv(o.harmonisation, index=False)
plausibility(i.universe, dict(zip(P.sources, i.events)), P.batch_rows).to_csv(
    o.plausibility, index=False
)
