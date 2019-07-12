#!/usr/bin/env bash

# Author: Ilya Kisil <ilyakisil@gmail.com>

# Source project wide setup variables
source variables.sh

# Check for anaconda first, so not to contaminate users environment
if [[ -x "$(command -v conda)" ]]; then
    # Create venv with conda
    conda create -y --name ${VENV_NAME} python=3.6.5

    # Replicate binder build process
    source activate ${VENV_NAME}
    pip  install -r ${PROJECT_HOME}/requirements.txt
    sh -c "postBuild --local-build"
    source deactivate
else
    printf "\n\n"
    printf "==> WARNING: Could not find anaconda installation!!!\n\n"
    printf "Install anaconda and rerun this script.\n"
    printf "\n\n"
fi