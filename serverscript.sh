#!/usr/bin/env bash
shpath="$(dirname "$(readlink -f "$0")")"
[ -f "$shpath/../chadnet-wiki.tar" ] && rm "$shpath/../chadnet-wiki.tar" && echo 'Removed old tar file'
sed -i "s/<p>Download <a href=\"chadnet-wiki.tar\".*/<p>Wiki is being updated. Archive is still being generated. Refresh the page in one minute to download the archive.<\/p>/" "$shpath/../index.html"
shopt -s extglob
chmod 644 $shpath/../!(tools)
chmod 755 $shpath/../files/
chmod 644 $shpath/../files/*
echo 'Changed file permissions'
echo 'Creating tar file...'
time tar --exclude="$shpath/../chadnet-wiki.zip" \
--sort=name \
--mtime='2012-12-12' \
--owner=0 --group=0 --numeric-owner \
--pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
-cf "$shpath/../chadnet-wiki.tar" $shpath/../*
echo 'Created tar file'
sed -i "s/<p>Wiki is being updated. Archive is still being generated.*/<p>Download <a href=\"chadnet-wiki.tar\">.tar archive<\/a> ($(bc <<< "scale=2; $(ls -l "$shpath/../chadnet-wiki.tar" | awk '{ print $5 }')/1024^3") GB) of the wiki\! <a href=\"tar.html\">(How to open .tar)<\/a><\/p>/" "$shpath/../index.html"
