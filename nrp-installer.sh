#!/bin/bash

# This script installs the NRP repository tools

# Environment variables
# PYTHON:
#              python executable to use for installation and running the NRP tools
# NRP_GIT_URL:
#              URL of the NRP git repository
# NRP_GIT_BRANCH:
#              branch of the NRP git repository to use
# LOCAL_NRP_DEVTOOLS_LOCATION:
#              location of the local NRP repository.
#              If set, do not clone the NRP repository but use the local one.

set -e

NRP_GIT_URL=${NRP_GIT_URL:-https://github.com/oarepo/nrp-devtools.git}
NRP_GIT_BRANCH=${NRP_GIT_BRANCH:-main}

SUPPORTED_PYTHON_VERSIONS=(3.10 3.9)

if [ -z "$PYTHON" ] ; then

  # find a supported python
  for version in "${SUPPORTED_PYTHON_VERSIONS[@]}"; do
      if command -v python$version >/dev/null 2>&1; then
          PYTHON=python$version
          break
      fi
  done

  if [ -z "$PYTHON" ] ; then
    echo "No supported python version found. Please install python 3.9 or higher
    or set the PYTHON environment variable to the python executable."
    exit 1
  fi
fi

# clone nrp tool to a temporary directory
ACTUAL_DIR="$(pwd)"
TMP_DIR=$(mktemp -d)

trap 'rm -rf "$TMP_DIR"' EXIT

echo "Installing temporary NRP CLI to $TMP_DIR, will clean it up on exit."


$PYTHON -m venv "$TMP_DIR/.venv"
source "$TMP_DIR/.venv/bin/activate"
pip install -U setuptools pip wheel

if [ -z "$LOCAL_NRP_DEVTOOLS_LOCATION" ] ; then
  LOCAL_NRP_DEVTOOLS_LOCATION="$TMP_DIR/nrp-devtools"
  git clone "$NRP_GIT_URL" --branch "$NRP_GIT_BRANCH" --depth 1 "$LOCAL_NRP_DEVTOOLS_LOCATION"
fi
pip install -e "$LOCAL_NRP_DEVTOOLS_LOCATION"

"$TMP_DIR"/.venv/bin/nrp-devtools initialize "$@"
