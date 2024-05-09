#!/bin/bash
# Script to run a job on a medium LSF node for 24 hours

# Default values for -n and -M
num_cores=1
memory=8

# Check for command line arguments and update accordingly
while getopts "n:M:" opt; do
  case $opt in
    n) num_cores=$OPTARG;;
    M) memory=$OPTARG;;
    \?) echo "Invalid option: -$OPTARG" >&2; exit 1;;
  esac
done

bsub -XF -Is -u swu12@mdanderson.org -N -q short -W 3:00 -n ${num_cores} -M ${memory} -R rusage[mem=${memory}] /bin/bash
