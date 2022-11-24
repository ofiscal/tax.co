# What these files are

## The pictures

`change-in.<variable>.by-<subsample>.<strategy>.png` is a picture, depicting how much `variable` would change across subsample `subsample`, given strategy `strategy`, compared to the baseline (the law as it currently is). `strategy` is whatever you chose when you ran the simulation. `subsample` might be `earners`, or `households`, etc. -- see the section of this README called `Subsamples` below. The only value that `variable` currently takes is mean income tax, but that could change in the future.

## The tables

Each table describes some subsample. Each row of the table describes a summary statistic of some variable -- e.g. mean income, or min income, or maximum paid in IVA, etc. Each row describes some subset of that population -- women, people in Neiva, people in the top 1% of income earners, etc.

The files called `report_<subsample>.<strategy>.<year>.<extension>` are all tables. Each comes in two formats (determined by `extension`): `csv` and `xls` (Excel).  The `strategy` is, again, whatever you chose when you ran the model. The `subsample` is, again, the subsample that the table describes; see the section of this README called `Subsamples` below.

Each table comes in two flavors, `tmi` and not `tmi`. Both are the same, except that `tmi` contains more rows (more summary statistics).

### PITFALL: The meaning of the income quantiles depends on the subsample.

For almost every subsample, the income quantiles are based on total income. However, for the `nonzero laborers` subsample, the income percentiles are based instead on labor income.


# Subsamples

`Households` is the full sample -- every hosueholds. It constitutes the entire data set. The unit of observation in `households` is not a person but rather a group of people living together, as defined by the Encuesta Nacional de Presupuestos de Hogares.

`HouseholdsFemale` is a subset of `households` containing only those households for which the head of household is female. `HouseholdsMale` is similar, containing households for which the head of household is male.

All the other samples are of individuals, rather than households.

`Earners` contains all *potential* earners. It includes everyone whose income is nonzero, *and* everyone who is at least 18 years old and in the labor force. It includes unemployed adults and working children.

`EarnersFemale` and `EarnersMale` are self-explanatory.

`Nonzero laborers` is a subset of `earners` that includes only people whose income is greater than zero. So it still includes working children, but it does not include unemployed adults. (Neither sample includes unemployed children.) Note that, as explained above (under `The meaning of the income quantiles depends on the subsample`), the income quantiles for this subsample are based on labor income, whereas in every other subsample they are based on total income.
