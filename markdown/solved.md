These are Some bugs that were fixed in the testing process.

I read changes backwards from today (Jan 16, 2020) (May 23, 2019).
There are surely more before that, but I feel like this proves the point.

# commit d59d88fb11ec56c02933d5a93cfccafcc7e6d335
build.purchases.main: drop non-positive quantities. (This was a bug in the data, not the code.)

# commit 8b17e23729ce89f1fcfd9068e7db5425c11033b7
common.cl_args: delete a dangerous default argument. Better to always specify subsample at the call site.

Otherwise, when running the code by hand (rather than via make), the subsample used in one file might not correspond to that of another.

# commit e5125a7407d3ab662f58e5a53e22c83420a174f6
Set random seed when subsampling. Otherwise subsample results are not be stable across runs.

# commit c2845426bcf398068d5451bfe6672865fb5dae08
Discover some problems:
  * there are purchases for which quantity=0
  * max vat is 0.27
  * max (vat frac) does not correspond to max (vat)
  * upon failure, the logging idiom does not capture what failed

# commit b2121bc56d5818cecd4d50c438df8711f2286de1
buildings: always use full samples, for two reasons:

* If it was subsampled at 1/n, and another file was as well,
  then  their merge would be subsampled at roughly 1/n^2.
* Missing data causes the smallest subsample to be read as an int,
  while larger subsamples are read as floats.

# commit 272fc605b1861e546b6cc0e860467049c0b377ed
rename freq -> per month
  "freq" is ambiguous -- it could use another denominator,
  or it could be the frequency codes DANE uses.

# commit c596f3db3c45f09a4b9f0b68820e4d22dd5abc1d
Done: Rewrite so that all IO comes at the end.
  Otherwise `make` might think something is built when it is not,
  and thus fail to rebuild it, and everything downstream would be wrong.

# commit 500b76cf5821228ba63c4f4e1efe3cee7f586659
Discover, document a bug (still unsolved):
  * In people (full sample)        max household member is 22
  * But in purchases (full sample) max household member is 195

# commit 1a631df273aafdf50c0090f32999cbd708fc891d
## bugfix: race flags
They were being compared to numeric values after the original race variable
had been converted to stringish categorical values.

## identify a potential bug
"income, private, in-kind" is always 0

# commit 9359e17b949fa8da5bd23cb179dfc16b6839dcba

## bugfix in `Correction.Replace_Substring_In_Column`
Preserve missing values, rather than replacing them with "nan".
(A string that says "nan" is not treated as

## drop "never" frequencies and non-positive quantities
in python.build.purchases_2_vat

# commit 006cc70278871ff3ea5c4e289fc242490375c792
`util.pad_column_as_int`: bugfix
  so that it does not create invalid number-string hybrids

# commit d78f233137663c0da46abd0faac5ce92c863ebdf
bugfix in `common.misc.all_columns_to_numbers`: 
  Convert all values to str before replacing "" and "nan" with np.nan.

Otherwise many that should be changed are not.
