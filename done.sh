#!/usr/bin/env bash
shpath="$(dirname "$(readlink -f "$0")")"
mv -iv $shpath/out/*.html ..
find $shpath/out/files/ ! -name 'xmas.gif' -type f -exec mv -iv {} $shpath/../files/ \;
cat $shpath/db >> $shpath/../db.chad
rm $shpath/db
