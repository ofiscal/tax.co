#!/bin/bash

# There is only one variety of the detail strategy.
echo; echo detail; date
make overview subsample=$1 vat_strategy=detail

# For each of the others we can specify some constant tax rates.
for vat_strategy in approx; do
    for vat_flat_rate in 0.19 0.18; do
        echo; echo $vat_strategy $vat_flat_rate; date
        make overview subsample=$1 vat_strategy=$vat_strategy vat_flat_rate=$vat_flat_rate
    done
done

# That list of tax rates can be empty, in which case the loop does nothing.
for vat_strategy in prop-2018-11-31; do
    for vat_flat_rate in 0.17; do
        echo; echo $vat_strategy $vat_flat_rate; date
        make overview subsample=$1 vat_strategy=$vat_strategy vat_flat_rate=$vat_flat_rate
    done
done

for vat_strategy in const; do
    for vat_flat_rate in; do
        echo; echo $vat_strategy $vat_flat_rate; date
        make overview subsample=$1 vat_strategy=$vat_strategy vat_flat_rate=$vat_flat_rate
    done
done

echo; date; echo
