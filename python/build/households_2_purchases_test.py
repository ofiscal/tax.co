# The sum of the columns from the purchase-sum data should be the same
# in both the purchase-sum and the hh data sets.
  # Exception: for "vat paid, min" and "vat paid, max",
  # the sum in the hh data should be the same as the sum in the purchase
  # data excluding San Andres.
  # Such a test would require pulling geo data into the purchase-sum data.
  # However, since those purchase-sum variables are not treated differently
  # from "transactions" or "value" by households_2_purchases.py,
  # it is safe (and faster) to simply omit
  # "vat paid, min" and "vat paid, max" from the test.

