#!/bin/bash

for strategy in detail; do
  for year in 2016 2018; do
    echo; echo "strategy:" $strategy $year; date
    make overview subsample=$1 \
                  regime_year=$year \
                  strategy=$strategy
  done
done

echo; date; echo
