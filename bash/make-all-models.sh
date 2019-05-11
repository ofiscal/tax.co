#!/bin/bash

for strategy in detail; do
    echo; echo $strategy; date
    make overview subsample=$1 strategy=$strategy regime_year=2016
done

echo; date; echo
