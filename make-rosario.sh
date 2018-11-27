#!/bin/bash

# Arguments:
# $1 = reciprocal of subsample size (1,10,100,1000)
# $2 = exemption source (auto or manual, without quotation marks)
# $3 = exemption count (she originally imagined 5, 10 or 20)

echo date
make overview -f Makefile.del_rosario subsample=$1 vat_strategy=del_rosario del_rosario_exemption_source=$2 del_rosario_exemption_count=$3
