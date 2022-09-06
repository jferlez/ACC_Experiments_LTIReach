#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ..
git pull
cd "$SCRIPT_DIR"
charmrun +p1 run_experiment.py TLLExperimentGroup20220906001140.p
ssh 10.0.0.10 "mkdir -p /media/azuredata/minion27"
scp -r ~/acc23ltireach/minion27 10.0.0.10:/media/azuredata/minion27
pwsh ~/shutdown_self.ps1
