#!/bin/bash

vatStrategy=detail
vatFlatRate=""
filename="overview, tmi.""$vatStrategy"_"$vatFlatRate".csv

from=output/vat/tables/recip-$1
to=output/vat/tables/prev/recip-$1

cp "$from/$filename" "$to/$filename"
