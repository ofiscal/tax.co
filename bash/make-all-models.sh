#!/bin/bash

for strategy in detail; do
    echo; echo $strategy; date
    make overview subsample=$1 \
                  regime_year=$2 \
                  strategy=$strategy
done

echo; date; echo
