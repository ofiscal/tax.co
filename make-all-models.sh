#!/bin/bash

make overview subsample=$1 vat_strategy=approx
make overview subsample=$1 vat_strategy=detail
make overview subsample=$1 vat_strategy=const vat_const_rate=0.19
make overview subsample=$1 vat_strategy=const vat_const_rate=0.17
make overview subsample=$1 vat_strategy=const vat_const_rate=0.16
make overview subsample=$1 vat_strategy=const vat_const_rate=0.107
