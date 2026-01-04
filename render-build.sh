#!/usr/bin/env bash
set -e

mkdir -p ephe

BASE="https://www.astro.com/ftp/swisseph/ephe"

curl -L -o ephe/sepl_18.se1   "$BASE/sepl_18.se1"
curl -L -o ephe/semo_18.se1   "$BASE/semo_18.se1"
curl -L -o ephe/seas_18.se1  "$BASE/seas_18.se1"
