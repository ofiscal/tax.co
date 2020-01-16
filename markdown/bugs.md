These are bugs or potential bugs remaining to be addressed.

# possibly wrong
## BLOCKED : "household member" max mismatch
### awaiting response from Juan, who awaits from DANE
### the problem
  No variable in the data has the properties that a household-member variable would need.
  see python/explore/what-is-household-member/
### do we really need those person identifiers?
  Is Orden unique within households in the person data?
## If max vat is 0.27, max vat frac should be 0.213
  but instead it's 0.160, which is what would derive from a max vat of 0.19.
  This problem arises in `purchases_2_vat_test.py`
## why are the median columns in overview.py's df_tmi called "unweighted"?
## add cesantias + primas to (which?) income measure
   should be in denominator, and not numerator, of tax rate.
   formality matters
     if an informal person makes 500K, they don't get primas + cesantias
## sanity checks: are these two variables ever both > 0 ?
That would mean someone was in both school and university.
### P5180S1, P5180S2 : daily payment for, value of food at school
### P6180S1, P6180S2 : daily payment for, value of food at university
## purchases.main: what to do|is done about missing freq, where-got, is-purchase
 is-purchase we probably assume to be 1, but the others ...?
 (they are often missing)
## "vat" conflates some taxes
  That's why, for instance, its max in purchases_2_vat_test is 0.27, not 19
## how bad is capitulo c?
  The following bullet items were written at two different times.
  They contradict each other.
### more than 2/3 of the "capitulo c" observations have no associated value
#### and they are only divided into 25 broad categories, with no associated quantity variable, so imputation is infeasible
#### Those value-missing observations are 19.2% of our data.
   Hopefully that will be close to 0 after discarding:
     frequency = nunca
     ~ bought it in the last week
     value = 99
### most purchases use coicop, not capitulo c codes
   capitulo c is a very small fraction of total purchases
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
## assumption: set "where got" to "purchase"
  in build/purchases/capitulo_c.py
  (it's currently unset)
# definitely unsafe
## use the UVT rather than fixed peso amounts
## handle csv format outside of pandas
  document everything below, then merge the branch into `tests`
### motivating example
  in ./build/vat_rates.py:
    vat_coicop = pd.read_csv( "data/vat/" + "vat-by-coicop.csv"
                            , sep = ";" # TODO PITFALL
                            , encoding = "latin1" )
### document or add to the preliminary Makefile
   apt install csvtool
   mv data/enph_2017/2_unzipped/csv -> /ssv
   mkdir 3_csv
   cd 2_unzipped/ssv
   for i in *; do csvtool -t ';' -u ',' cat $i -o ../../3_csv/$i; done
### csvtools deletes whitespace between separators
   For those values, the ssv files read as strings,
   while the csv files read as NaN.
### csvtool converts numbers containing commas to strings
