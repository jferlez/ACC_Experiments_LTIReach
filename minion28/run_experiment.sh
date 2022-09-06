#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ..
git pull
cd "$SCRIPT_DIR"
charmrun +p1 run_experiment.py TLLExperimentGroup20220906001140.p
ssh 10.0.0.10 "mkdir -p /media/azuredata/minion28"
scp -r ~/acc23ltireach/minion28 10.0.0.10:/media/azuredata/minion28
pwsh ~/shutdown_self.ps1
