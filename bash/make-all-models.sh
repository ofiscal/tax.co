#!/bin/bash

for strategy in vat_holiday_3 detail; do
  for year in 2018; do # 2016 2018
    echo; echo "strategy:" $strategy $year; date
    make tests overview subsample=$1 \
                        regime_year=$year \
                        strategy=$strategy
  done
done

echo; date; echo
