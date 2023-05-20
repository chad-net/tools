#!/bin/bash

# run file from anywhere
shpath="$(dirname "$(readlink -f "$0")")"
pushd $shpath > /dev/null

python3 -m wiki.main

popd > /dev/null
