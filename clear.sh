#!/bin/bash
shpath="$(dirname "$(readlink -f "$0")")"
rm -v $shpath/out/*.html
find $shpath/out/files/ ! -name 'xmas.gif' -type f -exec rm -v {} +
> $shpath/db
