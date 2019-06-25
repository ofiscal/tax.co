#!/bin/bash

for strategy in detail; do
  for year in 2016; do # 2016, 2018
    echo; echo "strategy:" $strategy $year; date
    make tests subsample=$1 \
                        regime_year=$year \
                        strategy=$strategy
  done
done

echo; date; echo
