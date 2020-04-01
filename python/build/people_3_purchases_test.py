twice, load people = oio.readStage( c.subsample, "people_2_buildings" )
  first, load one row, and call it "columns"
  then, load all rows but only one column, and call it "rows"
load one row of purchase_sums, and call it "columns" also
load people_3_purchases (entirely)

check that people_3 has the same number of rows as people_2
check that the columns are expanded per below

check VAT min, max in San Andrés (accent is important) is 0.
check that location is San Andrés sometimes (to ensure no misspelling).
check that these new variables have reasonable distributions
  people["vat/value, min" ] = people["vat paid, min"] / people["value" ]
  people["vat/value, max" ] = people["vat paid, max"] / people["value" ]
  people["vat/income, min"] = people["vat paid, min"] / people["income"]
  people["vat/income, max"] = people["vat paid, max"] / people["income"]
  people["value/income"   ] = people["value"]         / people["income"]
  people["income-decile"] =
  people["female head"] = people["female"] * (people["household-member"]==1)

