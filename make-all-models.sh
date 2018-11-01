#!/bin/bash

make overview subsample=$1 vat_strategy=approx
make overview subsample=$1 vat_strategy=detail
make overview subsample=$1 vat_strategy=const vat_flat_rate=0.19
make overview subsample=$1 vat_strategy=const vat_flat_rate=0.17
make overview subsample=$1 vat_strategy=const vat_flat_rate=0.16
make overview subsample=$1 vat_strategy=const vat_flat_rate=0.107
make overview subsample=$1 vat_strategy=prop-2018-11-31 vat_flat_rate=0.18
make overview subsample=$1 vat_strategy=prop-2018-11-31 vat_flat_rate=0.17
make overview subsample=$1 vat_strategy=prop-2018-11-31 vat_flat_rate=0.16
make overview subsample=$1 vat_strategy=prop-2018-11-31 vat_flat_rate=0.15

