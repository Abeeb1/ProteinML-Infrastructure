import json
import os
import subprocess
import sys
from datetime import datetime, timezone


FIELDS = [
    "job_id", "state", "elapsed",
    "total_cpu", "max_rss", "exit_code"
]


def parse_sacct(output):
    rows = []

    for line in output.splitlines():
        values = line.split("|")

        if len(values) == len(FIELDS):
            rows.append(dict(zip(FIELDS, values)))

    return rows


def collect_metrics(job_id):
    result = subprocess.run(
        [
            "sacct",
            "-j", str(job_id),
            "--noheader",
            "--parsable2",
            "--format=JobID,State,Elapsed,TotalCPU,MaxRSS,ExitCode",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return {
        "slurm_job_id": str(job_id),
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "steps": parse_sacct(result.stdout),
    }


def main():
    job_id = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.environ.get("SLURM_JOB_ID")
    )

    if not job_id:
        raise SystemExit("Usage: python collect_metrics.py JOB_ID")

    report = collect_metrics(job_id)

    if not report["steps"]:
        raise SystemExit(f"No accounting records found for job {job_id}")

    os.makedirs("metrics", exist_ok=True)
    output = f"metrics/job_{job_id}.json"

    with open(output, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Metrics saved to {output}")


if __name__ == "__main__":
    main()
