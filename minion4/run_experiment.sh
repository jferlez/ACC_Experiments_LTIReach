#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ..
git pull
cd "$SCRIPT_DIR"
/usr/local/bin/charming run_experiment.py TLLExperimentGroup20220906001139.p
ssh 10.0.0.10 "mkdir -p /media/azuredata/minion4"
scp -r ~/acc23ltireach/minion4 10.0.0.10:/media/azuredata/minion4
pwsh ~/shutdown_self.ps1
