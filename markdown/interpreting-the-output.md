# What these files are

These are the results of the tax microsimulation you ran. Some of them say what would happen in the scenario you specified. Others, which have "change" in the name, compare what would happen under the scenario you specified to what would happen given current tax law.

## The pictures

`change-in.<variable>.by-<sample>.<strategy>.png` is a picture, depicting how much `variable` would change across `sample`, given `strategy`, compared to the baseline (the law as it currently is). `strategy` is whatever you chose when you ran the simulation. `sample` might be `earners`, or `households`, etc. -- see the section of this README called `Samples` below.

Currently, the only value that `variable` currently takes is mean income tax, but that could change in the future.

## The tables

The files called `report_<sample>.<strategy>.<year>.<extension>` are all tables. Each table describes some sample. Each row of the table describes a summary statistic of some variable -- e.g. mean income, or min income, or maximum paid in IVA, etc. Each column describes some subsample of the sample -- women, people in Neiva, people in the top 1% of income earners, etc.

Each table comes in two formats (determined by `extension` in the filename): `csv` and `xls` (Excel).  The `strategy` in the name is whatever you chose when you ran the model. The `sample` in the name is the sample that the table describes; see the section of this README called `Samples` below.

Each table comes in two flavors, `tmi` and not `tmi`. Both are the same, except that `tmi` contains more rows (more summary statistics).

### PITFALL: The meaning of the income quantiles depends on the sample.

For almost every sample, the income quantiles are based on total income. However, for the `nonzero_earners_by_labor_income` sample, the income percentiles are based instead on labor income. Similarly, `households_by_income_per_capita`, the the income percentiles are based instead on income per capita (i.e. the household's total income, divided by number of people in the household).


# Samples

`Households` is the full sample -- every hosueholds. It constitutes the entire data set. The unit of observation in `households` is not a person but rather a group of people living together, as defined by the Encuesta Nacional de Presupuestos de Hogares.

`households_by_income_per_capita` is the same sample as `households`, but it defines its income quantiles differently, as described above.

`HouseholdsFemale` is a subset of `households` containing only those households for which the head of household is female. `HouseholdsMale` is similar, containing households for which the head of household is male.

All the other samples are of individuals, rather than households.

`Earners` contains all *potential* earners. It includes everyone whose income is nonzero, *and* everyone who is at least 18 years old and in the labor force. It includes unemployed adults and working children.

`EarnersFemale` and `EarnersMale` are self-explanatory.

`nonzero_earners_by_labor_income` is a subset of `earners` that includes only people whose income is greater than zero. Thus, like `earners`, it includes working children, but it does not include unemployed adults. (Neither sample includes unemployed children.) As explained above under `The meaning of the income quantiles depends on the sample`, the income quantiles for this sample are based on labor income, not total income.
