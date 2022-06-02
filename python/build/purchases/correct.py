if True:
  import numpy as np
  from itertools import chain
  #
  from   python.build.classes import Correction
  import python.build.output_io as oio
  import python.build.purchases.correct_defs as defs
  import python.common.common as cl
  import python.common.misc as com
  #
  # input files
  import python.build.purchases.nice_purchases as nice_purchases
  import python.build.purchases.articulos as articulos
  import python.build.purchases.capitulo_c as capitulo_c


purchases = oio.readCommonOutput (
  cl.subsample,
  'purchases_0' )

for c in (
    # PITFALL: Any correction reliant on a column's being a number
    # cannot be trusted to work here. Put it later in the program,
    # after running `all_columns_to_numbers`.
  [ Correction.Replace_Substring_In_Column(
      "quantity", ",", "." )
  , Correction.Replace_Missing_Values(
      "quantity", 1 )
  , Correction.Replace_Missing_Values(
      "per month", 1 )
  , Correction.Change_Column_Type(
      "coicop", str )
  , Correction.Replace_Entirely_If_Substring_Is_In_Column(
      "coicop", "inv", np.nan )
  ] + list(
        chain.from_iterable( [
          # chain.from_iterable concatenates its argument's members
          [ Correction.Change_Column_Type( colname, str )
          , Correction.Replace_In_Column(
              colname
              , { ' ' : np.nan
                  # 'nan's are created from the cast to type str
                  , "nan" : np.nan } ) ]
          for colname in [ "where-got", "coicop", "per month"
                         , "how-got", "value"] ] ) )
  ): purchases = c.correct( purchases )

purchases = com.all_columns_to_numbers( purchases )
purchases = defs.drop_if_coicop_or_value_invalid( purchases )
purchases = defs.drop_absurdly_big_expenditures( purchases )
purchases = (
    Correction.Drop_Row_If_Column_Satisfies_Predicate(
        "value", lambda v: v <= 0 )
    . correct( purchases ) )
purchases = (
  Correction . # no "never" frequencies
  Drop_Row_If_Column_Satisfies_Predicate(
    "per month", lambda x: x==11 ) .
  correct( purchases ) )
purchases = (
  Correction . # no non-positive quantities
    Drop_Row_If_Column_Satisfies_Predicate(
      "quantity", lambda x: x<=0 ) .
  correct( purchases ) )


# These only make sense once the relevant columns are numbers.
for c in ( # how-got=1 -> is-purchase=1, nan -> nan, otherwise -> 0
  [ Correction.Apply_Function_To_Column(
      "how-got"
      , lambda x: 1 if x==1 else
        # PITFALL: x >= 0 yields False for NaN
        (0 if x >= 0 else np.nan) )
    , Correction.Rename_Column( "how-got", "is-purchase" )
    , Correction.Drop_Row_If_Column_Satisfies_Predicate(
      "quantity", lambda x: x <= 0 )
  ] ):
  purchases = c.correct( purchases )

oio.saveCommonOutput (
  cl.subsample,
  purchases,
  'purchases_1' )
