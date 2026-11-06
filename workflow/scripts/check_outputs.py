"""Clear results/out/ for transfer at the end of a run (see bpskit.transfer).

The verdict records THIS run. sync.sh pull does not trust it: it runs the same
check again over the bytes it is about to copy, because anything written to
results/out/ after this rule (a partial rerun, a single target) would
otherwise travel under an old PASS.
"""

import sys
from pathlib import Path

from bpskit import transfer

# Snakemake entry point. Everything printed, and any traceback, goes to the
# rule's log, which is what sync.sh brings back from the data machine.
sys.stdout = sys.stderr = open(snakemake.log[0], "w", buffering=1)  # noqa: SIM115
verdict = Path(snakemake.output[0])
# The verdict lives at results/out/run/; the tree it clears is results/out/.
ids = transfer.load_ids(snakemake.input.ids)
# Column names that make a table per-person: internal keys and the delivery's
# own id and date columns.
forbidden = transfer.forbidden_columns(
    {"universe": snakemake.params.universe, "sources": snakemake.params.sources}
)
n, problems = transfer.check(
    [verdict.parents[1]], ids, strict=True, forbidden=forbidden, skip=[verdict]
)
text = (
    "REFUSED\n" + "\n".join(problems) + "\n"
    if problems
    else f"PASS: {n} files checked against {len(ids):,} patient ids\n"
)
verdict.write_text(text)
print(text)
if problems:
    sys.exit(1)
