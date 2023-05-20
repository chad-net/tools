#!/bin/bash
# you can do the following: alias wiki='source ~/wiki_dir/tools/wiki.sh'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
python -m wiki.main
