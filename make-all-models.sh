#!/bin/bash

# The implemented strategies for computing a coicop-vat bridge are these:
# detail
# detail_224
# approx
# finance_ministry
# prop_2018_10_31
# const
# PITFALL: run "del_rosario" from a different make-*.sh script, not this one

# PITFALL: Valid vat_flat_rate values decimals in [0,1] -- not, e.g., 19.

# Note that a loop below might "loop" over zero items.

# There is only one variety of the detail, detail_224 and finance_ministry strategies.
for vat_strategy in detail detail_224; do
    echo; echo $vat_strategy; date
    make overview subsample=$1 vat_strategy=$vat_strategy
done

# For each of the other strategies, we can specify some constant tax rates.
for vat_strategy in const prop_2018_10_31; do
    for vat_flat_rate in; do
        echo; echo $vat_strategy $vat_flat_rate; date
        make overview subsample=$1 vat_strategy=$vat_strategy vat_flat_rate=$vat_flat_rate
    done
done

echo; date; echo
