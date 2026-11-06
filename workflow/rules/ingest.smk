# The people file into the universe, each diagnosis file into harmonised
# events, the quality tables, and the transfer check.


rule universe:
    input:
        socio=f"{config['delivery_root']}/{config['universe']['file']}",
    output:
        universe="results/work/universe.parquet",
        ids="results/work/ids/universe.parquet",
        summary="results/out/tables/universe_summary.csv",
    log:
        "results/work/logs/universe.log",
    conda:
        "../envs/bpskit.yaml"
    resources:
        mem_mb=6000,
    params:
        universe=config["universe"],
        sentinels=config["sentinels"],
        mid_month_day=config["mid_month_day"],
        buckets=config.get("buckets"),
    script:
        "../scripts/universe.py"


rule ingest_source:
    input:
        file=lambda wc: f"{config['delivery_root']}/{config['sources'][wc.source]['file']}",
        universe="results/work/universe.parquet",
    output:
        events="results/work/events/{source}.parquet",
        episodes="results/work/events/{source}.episodes.parquet",
        qc="results/work/qc/harmonisation_{source}.csv",
        ids="results/work/ids/{source}.parquet",
    log:
        "results/work/logs/ingest_source/{source}.log",
    conda:
        "../envs/bpskit.yaml"
    resources:
        mem_mb=8000,
    params:
        source=lambda wc: config["sources"][wc.source],
        sentinels=config["sentinels"],
        mid_month_day=config["mid_month_day"],
        map_icd9=config["map_icd9"],
        records=config["records"],
        scale=config["scale"],
    script:
        "../scripts/ingest_source.py"


rule quality:
    input:
        qc=expand("results/work/qc/harmonisation_{source}.csv", source=SOURCES),
        events=expand("results/work/events/{source}.parquet", source=SOURCES),
        universe="results/work/universe.parquet",
    output:
        harmonisation="results/out/tables/quality/harmonisation.csv",
        plausibility="results/out/tables/quality/plausibility.csv",
    log:
        "results/work/logs/quality.log",
    conda:
        "../envs/bpskit.yaml"
    resources:
        mem_mb=4000,
    params:
        sources=SOURCES,
        batch_rows=config["scale"]["batch_rows"],
    script:
        "../scripts/quality.py"


# An analysis workflow importing this module overrides the input with its own
# final outputs (`use rule check_outputs from bps with: input: ...`), so the
# check runs after everything that writes to results/out/.
rule check_outputs:
    input:
        BPS_OUTPUTS,
        ids=expand("results/work/ids/{name}.parquet", name=["universe"] + SOURCES),
    output:
        "results/out/run/pullable_check.txt",
    log:
        "results/work/logs/check_outputs.log",
    conda:
        "../envs/bpskit.yaml"
    resources:
        mem_mb=4000,
    params:
        universe=config["universe"],
        sources=config["sources"],
    script:
        "../scripts/check_outputs.py"
