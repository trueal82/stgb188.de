#!/usr/bin/env bash

set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
site_dir="/var/www/stgb188.de"

if [[ ! -d "$site_dir" ]]; then
  echo "Target directory not found: $site_dir" >&2
  exit 1
fi

cd "$repo_dir"

git pull --ff-only

python3 build.py

rsync -a --delete "$repo_dir/static/" "$site_dir/"