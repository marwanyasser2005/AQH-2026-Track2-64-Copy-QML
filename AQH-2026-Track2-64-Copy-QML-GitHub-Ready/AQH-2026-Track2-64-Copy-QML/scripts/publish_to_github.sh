#!/usr/bin/env bash
set -euo pipefail
if [ $# -ne 1 ]; then echo "usage: $0 <git-remote-url>"; exit 2; fi
cd "$(dirname "$0")/.."
python scripts/validate_repo.py
if [ ! -d .git ]; then git init; git branch -M main; fi
git add .
git status
git commit -m "Consolidate AQH Track 2 V9.2 and V12 submissions"
if git remote get-url origin >/dev/null 2>&1; then git remote set-url origin "$1"; else git remote add origin "$1"; fi
git push -u origin main
