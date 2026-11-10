#!/usr/bin/env bash
set -euo pipefail

POLL_INTERVAL="${POLL_INTERVAL:-15}"
MAX_WAIT="${MAX_WAIT:-300}"

# Resume an existing job or submit a new one.
if [[ $# -ge 1 ]]; then
    job_id="$1"
    echo "Resuming monitoring for job: $job_id"
else
    job_id=$(sbatch --parsable run_container.sub)
    echo "Submitted Slurm job: $job_id"
fi

if ! [[ "$job_id" =~ ^[0-9]+$ ]]; then
    echo "Error: Invalid Slurm job ID: $job_id" >&2
    exit 2
fi

elapsed=0

while true; do
    state=$(sacct -j "$job_id" -X -n -P --format=State 2>/dev/null | head -n 1)
    state="${state%% *}"

    case "$state" in
        COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE)
            echo "Job finished with state: $state"
            break
            ;;
    esac

    reason=$(squeue -h -j "$job_id" -o "%r" | head -n 1)

    if [[ "$state" == "PENDING" ]]; then
        echo "Job pending. Reason: ${reason:-Unknown}"
    else
        echo "Job state: ${state:-Awaiting accounting data}"
    fi

    if (( elapsed >= MAX_WAIT )); then
        echo "Monitoring timeout reached after ${elapsed}s."
        echo "Slurm job $job_id has NOT been cancelled."
        echo "Resume later with: ./submit_and_monitor.sh $job_id"
        exit 124
    fi

    sleep "$POLL_INTERVAL"
    elapsed=$((elapsed + POLL_INTERVAL))
done

python collect_metrics.py "$job_id"

if [[ "$state" != "COMPLETED" ]]; then
    echo "Job did not complete successfully: $state" >&2
    exit 1
fi

echo "Monitoring completed successfully."
