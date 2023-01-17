#!/usr/bin/env bash
shpath="$(dirname "$(readlink -f "$0")")"
find $shpath/../ -type d \( -path $shpath \) -prune -o -exec chmod 644 {} \;

