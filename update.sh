#!/usr/bin/env bash
shpath="$(dirname "$(readlink -f "$0")")"
perl -i -pe "s/<p>Total links: <strong>.*$/<p>Total links: <strong>$(cat "$shpath/CHADNET_LINK_COUNT")<\/strong>. Last updated on $(date --utc +'%B %d, %Y, at %H:%M UTC').<\/p>/" "$shpath/../index.html"
echo "Updated index.html"
rm "$shpath/CHADNET_LINK_COUNT"
shopt -s extglob
chmod 644 $shpath/../!(tools)
chmod 755 $shpath/../files/
chmod 644 $shpath/../files/*
echo "Changed file permissions"
