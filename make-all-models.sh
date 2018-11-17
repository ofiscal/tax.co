#!/bin/bash

echo; date; echo
make overview subsample=$1 vat_strategy=detail
echo; date; echo
#make overview subsample=$1 vat_strategy=approx vat_flat_rate=0.19
echo; date; echo
make overview subsample=$1 vat_strategy=approx vat_flat_rate=0.18

echo; date; echo
#make overview subsample=$1 vat_strategy=prop-2018-11-31 vat_flat_rate=0.18
echo; date; echo
#make overview subsample=$1 vat_strategy=prop-2018-11-31 vat_flat_rate=0.17
echo; date; echo
#make overview subsample=$1 vat_strategy=prop-2018-11-31 vat_flat_rate=0.16
echo; date; echo
#make overview subsample=$1 vat_strategy=prop-2018-11-31 vat_flat_rate=0.15

echo; date; echo
#make overview subsample=$1 vat_strategy=const vat_flat_rate=0.18
echo; date; echo
#make overview subsample=$1 vat_strategy=const vat_flat_rate=0.17
echo; date; echo
#make overview subsample=$1 vat_strategy=const vat_flat_rate=0.16
echo; date; echo
#make overview subsample=$1 vat_strategy=const vat_flat_rate=0.107
echo; date; echo
