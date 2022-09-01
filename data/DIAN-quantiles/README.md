# To generate the `.csv` from these `.xlsx` files

See `./to-csv.py` demonstrates one way to do that.


# What these data are

DIAN will not provide individual-level data, for privacy reasons.
But it will provide data in which each observation (row)
is a quantile of some variable.
Each shee of the original `.xlsx` files represents a different
(year,variable,aggregated unit) triple.
The aggregated units are either individuals or firms.

The `.csv` data were generated from the `.xlsx` data.
Use those, not the `.xlsx` data,
unless I need more pages from the latter.

`2-cleaning.xlsx` is the same as `1-raw.xlsx`,
except that I've deleted rows and columns from certain pages,
in order to be able to convert them easily to `.csv` format.


## What the sheet names mean

Quoting Angie Nieto:
"""
Punto N means the way we asked for the milcil to be ordered.
Punto 1 and 2 is with a caculated variable I don't really understand,
so i dont use it.
Punto 3 is with quantiles computed based on patrimonio bruto.
Punto 4 is with quantiles computed based on patrimonio liquido.
Punto 6 y 7 are for personas juridicas.
"""
