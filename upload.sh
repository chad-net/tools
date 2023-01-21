#!/usr/bin/env bash
shpath="$(dirname "$(readlink -f "$0")")"
#number 1 sysadmin
rsync -vrPt --exclude='chadnet-wiki.tar' --delete $shpath/../. root@chadnet.org:/var/www/wiki/
ssh root@chadnet.org "
cd /var/www/wiki/tools/
chmod +x serverscript.sh
./serverscript.sh
"
scp root@chadnet.org:/var/www/wiki/index.html $shpath/../index.html
echo "Index updated"
