The ENPH consists of 16 files.
In most of those the unit of observation is a purchase.
This code collects all the purchase files we use
(we don't use real estate purchases, for reasons described elsewhere)
into a single file, and makes various reformattings,
homogenizations, and corrections.


# PITFALL: Assumptions and other modifications

This code assumes a number of things about the data it collects.
For instance, the following passage from `capitulo_c.py`:
```
capitulo_c_corrections = [
    Correction.Create_Constant_Column( "quantity", 1 )
  , Correction.Create_Constant_Column( "how-got", 1 )
  , Correction.Create_Constant_Column( "where-got", 1 )
  , Correction.Create_Constant_Column( "coicop", nan )
  , Correction.Drop_Row_If_Column_Equals( "duplicated", 1 )
  , Correction.Drop_Column( "duplicated" )
]
```
shows that we assume a quantity value of 1 for each purchase,
we assume it was purchased in a big store (i.e. where VAT is paid), etc.
Not all of these are assumptions, though -- some are definitionally true.
For instance, the "coicop" column is missing from the capitulo c data,
as it should be.
