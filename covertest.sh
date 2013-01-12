#! /bin/bash
set -e
export suite=${1}

coverage erase
coverage run $(which nosetests) -sv ${suite}
coverage report -m --include="*pydispatch*" 
