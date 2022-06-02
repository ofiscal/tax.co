household_variables_to_allocate_by_income_share = [
  "value, consumption",
  "value, non-purchase",
  "value, purchase",
  "value, spending",
  "value, tax, predial",
  "value, tax, purchaselike non-predial non-VAT",
  "value, tax, purchaselike non-VAT",
  "vat paid",
  ]

columns_to_pull_from_hs = ( [
  "household",
  "members in labor force",
  "income, household", # For allocating VAT among household members
                       # according to each member's income share.
  ] + household_variables_to_allocate_by_income_share )
