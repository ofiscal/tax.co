#!/bin/bash

for vat_strategy in detail; do
    echo; echo $vat_strategy; date
    make overview subsample=$1 vat_strategy=$vat_strategy
done

echo; date; echo
