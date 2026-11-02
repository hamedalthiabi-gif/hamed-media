#!/bin/sh
# Rebuild the live index.html: base (index.v1) -> home v3 -> series viewer -> inner pages
set -e
cd "$(dirname "$0")"
node homev3.js new/index.v1.html new/index.html
node series.js new/index.html
node inner.js new/index.html
node cal.js new/index.html
