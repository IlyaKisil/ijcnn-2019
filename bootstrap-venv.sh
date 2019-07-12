#!/usr/bin/env bash

# Author: Ilya Kisil <ilyakisil@gmail.com>

# Source project wide setup variables
# source ./variables.sh
PROJECT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
VENV_NAME="ijcnn-2019"
# Check for anaconda first, so not to contaminate users environment
if [[ -x "$(command -v conda)" ]]; then
    # Create venv with conda
    conda create -y --name ${VENV_NAME} python=3.6.5 pip

    # Replicate binder build process
    conda activate ${VENV_NAME}
    pip  install -r ${PROJECT_HOME}/requirements.txt
    sh -c "postBuild"
    # conda deactivate
else
    printf "\n\n"
    printf "==> WARNING: Could not find anaconda installation!!!\n\n"
    printf "Install anaconda and rerun this script.\n"
    printf "\n\n"
fi
