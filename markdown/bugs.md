This document is like a child of [goals.md](./goals.md).

These are bugs or potential bugs remaining to be addressed.

# Possibly wrong
## BLOCKED : "household member" max mismatch

Awaiting response from Juan, who awaits from DANE

### The problem
No variable in the data has the properties that a household-member variable would need.

See `python/explore/what-is-household-member/`

### Do we really need those person identifiers?
Is Orden unique within households in the person data?

## Bug ? If max vat is 0.27, max vat frac should be 0.213
But instead it's 0.160, which is what would derive from a max vat of 0.19.
This problem arises in `purchases_2_vat_test.py`

## Bug ? Why are the median columns in overview.py's df_tmi called "unweighted"?

## Bug ? Add cesantias + primas to (which?) income measure
Should be in denominator, and not numerator, of tax rate. 

Formality matters: if an informal person makes 500K, they don't get primas + cesantias.

## Bug ? Sanity checks: are these two variables ever both > 0 ?
That would mean someone was in both school and university.

* P5180S1, P5180S2 : daily payment for, value of food at school
* P6180S1, P6180S2 : daily payment for, value of food at university

## Bug ? purchases.main: what to do|is done about missing freq, where-got, is-purchase
Is-purchase we probably assume to be 1, but the others ...? (They are often missing.)

## Bug ? "vat" conflates some taxes
That's why, for instance, its max in purchases_2_vat_test is 0.27, not 19

## Bug ? How bad is capitulo c?
The following bullet items were written at two different times.
They contradict each other.

### more than 2/3 of the "capitulo c" observations have no associated value
and they are only divided into 25 broad categories, with no associated quantity variable, so imputation is infeasible.

Those value-missing observations are 19.2% of our data.
Hopefully that will be close to 0 after discarding these:

* frequency = nunca (they bought it in the last week)
* value = 99

### most purchases use coicop, not capitulo c codes
Capitulo c is a very small fraction of total purchases:
```
   >>> subsample = 10
   >>> purchases = oio.readStage( subsample, "purchases_2_vat" )
   >>> util.describeWithMissing( purchases[[[[ "25-broad-categs", "coicop"]] ]] )
            25-broad-categs        coicop
   0               0.000000  0.000000e+00
   length     689761.000000  6.897610e+05
   missing    657576.000000  3.218500e+04
   count       32185.000000  6.575760e+05
   mean           13.866801  4.833412e+06
   std             7.151346  4.292508e+06
   min             1.000000  1.110101e+06
   25%             7.000000  1.160111e+06
   50%            15.000000  1.220801e+06
   75%            20.000000  8.300305e+06
   max            25.000000  1.270990e+07
```

## Bug ? Impose assumption: set "where got" to "purchase"
In build/purchases/capitulo_c.py (it's currently unset).

# Definitely unsafe
## Unsafe ! Use the UVT rather than fixed peso amounts

## Unsafe ! Handle csv format together, once, upstream of the "conceptual" processing
