#!/bin/bash
# you can do the following: alias parser3000='source ~/wiki_dir/tools/parser3000.sh'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pushd "$SCRIPT_DIR" > /dev/null
python -m parser3000.main
popd > /dev/null
