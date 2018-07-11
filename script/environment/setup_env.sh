#!/usr/bin/env bash
set -euo pipefail
if ! python -m virtualenv --version; then
    >&2 echo "ERROR: Could not find available to the Python runtime, trying to install it"
    pip install virtualenv
    exit 1
fi

# set directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT=$(readlink -f "${SCRIPT_DIR}/../..")
VIRTUALENV_DIR="${PROJECT_ROOT}/venv"

# Instantiate the virtual envronment
echo "Creating user virtual environment in the PROJECT_ROOT (${PROJECT_ROOT}) in directory called 'venv'"
python -m virtualenv "${VIRTUALENV_DIR}"

# Install package requirements
set +u
echo "Stepping in to virtual environment in order to install dependencies"
# On windows, virtualenv has a slightly different format
# shellcheck source=/dev/null
if [[ -f "${VIRTUALENV_DIR}/Scripts/activate" ]]; then
    echo "Windows scripts virtualenv path taken"
    source "${VIRTUALENV_DIR}/Scripts/activate"
    echo "Windows virtualenv successfully loaded"
else
    source "${VIRTUALENV_DIR}/bin/activate"
fi
set -u
echo "Pip version:"
python -m pip --version
echo "Script dir: ${SCRIPT_DIR}"
echo "Project root: ${PROJECT_ROOT}"

python -m pip install pip

# Install requirements
START=$(date +%s)
python -m pip install --timeout=30 --retries=2 -r "${SCRIPT_DIR}/requirements.txt"
END=$(date +%s)
DIFF=$(( $END - $START ))
echo "pip install took $DIFF seconds"
echo "This is the end of execution (╯‵□′)╯︵┻━┻"
