# Checks the schema cannot express, and the paths this workflow produces.

import os

from snakemake.exceptions import WorkflowError

# A missing delivery must stop the run here. Left to Snakemake, a rule whose
# input is missing but whose output exists is skipped, so a wrong path would
# silently reuse the per-person intermediates of an earlier run.
if not os.path.isdir(config["delivery_root"]):
    raise WorkflowError(
        f"delivery_root {config['delivery_root']!r} does not exist (resolved from "
        f"{os.getcwd()}). Set it in config/config.yaml or, per machine, in "
        "profiles/default/config.yaml (copy profiles/default.example/)."
    )

SOURCES = list(config["sources"])


wildcard_constraints:
    source="|".join(SOURCES),


# What an analysis workflow can read, and lists in its own final outputs.
BPS_OUTPUTS = [
    "results/out/tables/universe_summary.csv",
    "results/out/tables/quality/harmonisation.csv",
    "results/out/tables/quality/plausibility.csv",
]
