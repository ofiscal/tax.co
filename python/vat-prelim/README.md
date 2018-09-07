# Pitfalls

If a vat subsample is used to generate statistics (including diagrams), some of those statistics might be NaN or Inf even though they would not be if generated from the full sample.


# Stages of data construction for the VAT

The VAT construction process involves a few stages. 

* 1.purchases.csv -- collects purchases across the different ENPH data sets. The unit of observation is a purchase.

* 2.purchases,prices,taxes.csv -- merges tax rates, via the match David magically provided between COICOP codes and tax rates.

* 3.person-level-expenditures.csv -- aggregates expenditures to the (household,household-member) level. (The unit of observation is defined by that pair of variables.)

* 4.demog.csv -- a subset of the demographic characteristics file. The unit of observation is a person, defined by that same pair of variables.

* 5.person-demog-expenditures.csv -- merges items 3 and 4.

* 6.households.csv -- aggregates people from 5.person-demog-expenditures.csv

Each of those 6 stages builds on each others. Each of the "stages" 7 through 9 build on some earlier products, but not necessarily all of them.
