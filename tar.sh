#!/usr/bin/env bash
shpath="$(dirname "$(readlink -f "$0")")"
shopt -s expand_aliases

[ -f "$shpath/../chadnet-wiki.tar" ] && rm "$shpath/../chadnet-wiki.tar" && echo "Removed old tar file"

echo "Creating tar file..."

[[ "$OSTYPE" == "darwin"* ]] && alias tar='gtar'
tar --sort=name \
--mtime="2012-12-12" \
--owner=0 --group=0 --numeric-owner \
--pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
-cf $shpath/../chadnet-wiki.tar $shpath/../*

echo "Tar file created"
