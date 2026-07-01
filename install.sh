#!/usr/bin/env bash

set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
service_name="stgb188-deploy.service"
timer_name="stgb188-deploy.timer"
systemd_dir="/etc/systemd/system"

if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
  echo "Run this script as root or with sudo." >&2
  exit 1
fi

install -m 0644 "$repo_dir/$service_name" "$systemd_dir/$service_name"
install -m 0644 "$repo_dir/$timer_name" "$systemd_dir/$timer_name"

systemctl daemon-reload
systemctl enable --now "$timer_name"

echo "Installed and enabled $timer_name"