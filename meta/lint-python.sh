#!/usr/bin/env bash

set -euo pipefail

script_path=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
project_root_dir=$(dirname $script_path)

pushd $project_root_dir

flake8 --ignore=F401,E501 --exclude .venv .
black --check .
#mypy .

popd
