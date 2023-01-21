#!/usr/bin/env bash
shpath="$(dirname "$(readlink -f "$0")")"
rsync -vrPt --exclude='chadnet-wiki.tar' --delete root@chadnet.org:/var/www/wiki/ "$shpath/../"
echo "Synced server to local"
