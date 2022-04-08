#!/bin/bash
PROJECT_ROOT=$(dirname "${BASH_SOURCE[0]}") 
cd ${PROJECT_ROOT}/../

test -f setup.cfg
python -m pytest
