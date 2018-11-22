#!/bin/bash

# The implemented strategies for computing a coicop-vat bridge are these:
# detail
# approx
# finance_ministry
# prop_2018_11_31
# const

# Note that a loop below might "loop" over zero items.

# There is only one variety of the detail and finance_ministry strategies.
for vat_strategy in finance_ministry; do
    echo; echo $vat_strategy; date
    make overview subsample=$1 vat_strategy=$vat_strategy
done

# For each of the other strategies, we can specify some constant tax rates.
for vat_strategy in; do
    for vat_flat_rate in; do
        echo; echo $vat_strategy $vat_flat_rate; date
        make overview subsample=$1 vat_strategy=$vat_strategy vat_flat_rate=$vat_flat_rate
    done
done

echo; date; echo
