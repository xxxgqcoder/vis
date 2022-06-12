#!/usr/bin/env bash
set -e

work_dir=$(dirname "$0")
cd ${work_dir}
echo "working directory $(pwd)"

cd _site

python -m http.server