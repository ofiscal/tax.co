The VAT construction process involves a few stages. 

* 1.purchases.csv -- this collects purchases across the different ENPH data sets. The unit of observation is a purchase.
* 2.purchases,prices,taxes.csv -- this merges tax rates, via the match David magically provided between COICOP codes and tax rates.
* 3.person-level-expenditures.csv -- This aggregates expenditures to the (household,household-member) level. (The unit of observation is defined by that pair of variables.)
* 4.demog.csv -- This is a subset of the demographic characteristics file. The unit of observation is a person, defined by that same pair of variables.
* 5.person-demog-expenditures.csv -- This merges items 3 and 4.
