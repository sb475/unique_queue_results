#!/usr/bin/env bash

set -euo pipefail

script_path=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
project_root_dir=$(dirname $script_path)

pushd $project_root_dir

bandit -x .venv -r .
