#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ..
git pull
cd "$SCRIPT_DIR"
charmrun +p1 run_experiment.py TLLExperimentGroup20220906001141.p
ssh 10.0.0.10 "mkdir -p /media/azuredata/minion39"
scp -r ~/acc23ltireach/minion39 10.0.0.10:/media/azuredata/minion39
pwsh ~/shutdown_self.ps1
