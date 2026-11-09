# ProteinML Infrastructure

A reproducible, containerized scientific computing workflow using Apptainer and Slurm on an HPC cluster.

## Project Overview

This project demonstrates how to package a Python application into an Apptainer container, deploy it on a Slurm-managed HPC cluster, and monitor execution performance.

The initial workload validates a Python and NumPy environment. The infrastructure is designed to support future scientific machine learning workloads.

## Technologies

- Linux and Bash
- Slurm Workload Manager
- Apptainer (Singularity)
- Python 3.11
- NumPy 1.26.4
- Git and GitHub

## Project Structure

```text
ProteinML-Infrastructure/
├── container.def
├── validate.py
├── run_container.sub
├── .gitignore
└── README.md
