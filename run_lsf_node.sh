#!/bin/bash
# Script to run a job on a medium LSF node for 24 hours

bsub -XF -Is -q short -W 3:00 -n 4 -M 32 -R rusage[mem=32] /bin/bash