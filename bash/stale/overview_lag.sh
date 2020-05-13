#!/bin/bash

subsample=$1
vatStrategy=$2
vatFlatRate=$3

filename="overview, tmi.""$vatStrategy"_"$vatFlatRate".csv
from=output/vat/tables/recip-"$subsample"
to=output/vat/tables/prev/recip-"$subsample"

cp "$from/$filename" "$to/$filename"
