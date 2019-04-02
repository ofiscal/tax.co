#!/bin/bash

# The implemented strategies for computing a coicop-vat bridge are defined
# in the "vat_strategy_names" variable in python.build.common.
# PITFALL: while most of those strategies should be run from this script,
# "del_rosario" runs from a different one.

# PITFALL: Valid vat_flat_rate values are decimals in [0,1] -- not, e.g., 19.

# Note that a loop below might "loop" over zero items.

# There is only one variety of the detail, detail_224, finance_ministry and prop_2018_11_29 strategies.
for vat_strategy in detail; do # detail_224 finance_ministry prop_2018_11_29
    echo; echo $vat_strategy; date
    make overview subsample=$1 vat_strategy=$vat_strategy
done

# For each of the other strategies, we can specify some constant tax rates.
for vat_strategy in; do #approx const prop_2018_10_31
    for vat_flat_rate in 0.18 ; do
        echo; echo $vat_strategy $vat_flat_rate; date
        make overview subsample=$1 vat_strategy=$vat_strategy vat_flat_rate=$vat_flat_rate
    done
done

echo; date; echo
