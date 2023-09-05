# Household-level and person-level income quantiles are different.
The simulation defines income quantiles
(deciles, percentile and milliles)
both for persons and for households.
These are *different things* --
a household could, for instance, be in the top income percentile,
even while one of the workers in it is in the bottom percentile.

# "IT" vs. "income"

For households we construct quantiles using DANE's "IT" aggregate,
while for people we use our own "income" aggregate.
That's because DANE's "IT" is only defined at the household level,
not the individual level.

For more on the difference between "income" and "IT", see
`household-and-person-level-total-income.md`.

# Certain reports use different measures yet

The `nonzero_earners_by_labor_income` reports use quantiles
detfined in terms of labor income.

The `households_by_income_per_capita` reports use quantiles
detfined in terms of IT per capita.
