#!/bin/bash
shpath="$(dirname "$(readlink -f "$0")")"
sed -i "s/<p>Total links: <strong>.*$/<p>Total links: <strong>$(cat "$shpath/CHADNET_LINK_COUNT")<\/strong>. Last updated on $(date --utc +'%B %d, %Y, at %H:%M UTC').<\/p>/" "$shpath/../index.html"
rm "$shpath/CHADNET_LINK_COUNT"
