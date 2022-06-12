#!/usr/bin/env bash
set -e

work_dir=$(dirname "$0")
cd ${work_dir}
echo "working directory $(pwd)"


rm -r _site/js || true

cp -r js _site/js

rm -r _site/css || true

cp -r css _site/css

cp favicon.ico _site

python generate_site.py \
    --work_dir=$(pwd) \
    --home_page="$(pwd)/index.html" \
    --pages_root_dir="$(pwd)/pages" \
    --out_root_dir="$(pwd)/_site"