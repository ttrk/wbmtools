#!/bin/bash

# Need to source this to run the python tools and connect to WBM

echo "exporting working directory to Python environment"
if [[ ! -z $PYTHONPATH ]]; then
  export PYTHONPATH=$PYTHONPATH:$PWD
fi
if [[ ! -z $PYTHON27PATH ]]; then
  export PYTHON27PATH=$PYTHON27PATH:$PWD
fi
if [[ ! -z $PYTHON3PATH ]]; then
  export PYTHON3PATH=$PYTHON3PATH:$PWD
fi

echo "exporting certificate to REQUESTS_CA_BUNDLE env var"
# Make sure the certificate is under wbmtools/, the base directory
fullPath=$(readlink -f ca-bundle.crt)
export REQUESTS_CA_BUNDLE=$fullPath

