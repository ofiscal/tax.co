import pandas as pd
from typing import Callable, Dict, List, Tuple

from python.common.misc import min_wage


def average_tax_function (
    fraction_of_wage      : float,
    min_base_in_min_wages : float,
    max_base_in_min_wages : float
) -> Callable [ [float], float ]:
  return ( lambda wage:
           min ( max ( wage     * fraction_of_wage,
                       min_wage * min_base_in_min_wages ),
                 min_wage       * max_base_in_min_wages ) )

def ss_tax_schedule_from_frame (
    df : pd.DataFrame
) -> List [
  Tuple [ float,                       # minimum income threshold
          Callable [ [float], float ], # computes taxable base from wage
          float ]]:                    # average (not marginal!) tax rate
  df["lambda"] = df.apply (
    lambda row: average_tax_function (
      row["fraction_of_wage"],
      row["min_base_in_min_wages"],
      row["max_base_in_min_wages"] ),
    axis = "columns" )
  return ( df [[ "min_threshold_in_min_wages",
                 "lambda",
                 "average_tax_rate" ]]
           . values . tolist () )

ss_contrib_schedule_for_contractor : Dict [
  str,
  List [ Tuple [ float, Callable [ [float], float ], float ] ] ] = {
  "pension" :
    [ ( 0, lambda _: 0, 0.0 )
    , ( min_wage
      , lambda wage: min( max( 0.4*wage, min_wage )
                        , 25*min_wage)
      , 0.16 ) ]
  , "salud" :
    [ ( 0
      , lambda wage: min( max( 0.4*wage, min_wage )
                        , 25*min_wage )
      , 0.125 ) ]
  , "solidaridad" :
    [ (0, lambda wage: 0, 0.0)
    , ( 4*min_wage
      , lambda wage: min( max(0.4*wage,min_wage)
                        , 25*min_wage)
      , 0.01)
    , ( 16*min_wage
      , lambda wage: min( max(0.4*wage,min_wage)
                        , 25*min_wage)
      , 0.012)
    , ( 17*min_wage
      , lambda wage: min( max(0.4*wage,min_wage)
                        , 25*min_wage)
      , 0.014)
    , ( 18*min_wage
      , lambda wage: min( max(0.4*wage,min_wage)
                        , 25*min_wage)
      , 0.016)
    , ( 19*min_wage
      , lambda wage: min( max(0.4*wage,min_wage)
                        , 25*min_wage)
      , 0.018)
    , ( 20*min_wage
      , lambda wage: min( max(0.4*wage,min_wage)
                        , 25*min_wage)
      , 0.02) ]
  }

ss_contrib_schedule_for_employee = {
  "pension" :
    [ ( 0,           lambda wage: 0                            , 0.0)
    , ( min_wage,    lambda wage: wage                         , 0.04)
    , ( 13*min_wage, lambda wage: min( 0.7*wage, 25*min_wage)  , 0.04 ) ]
  , "salud" :
    [ ( 0,           lambda wage: 0                            , 0.0 )
    , ( min_wage,    lambda wage: wage                         , 0.04 )
    , ( 13*min_wage, lambda wage: min( 0.7*wage, 25*min_wage ) , 0.04 ) ]
  , "solidaridad" :
    [ (0,            lambda wage:            0                 , 0.0)
    , (4*min_wage,   lambda wage:         wage                 , 0.01)
    , (13*min_wage,  lambda wage:     0.7*wage                 , 0.01)
    , (16*min_wage,  lambda wage:     0.7*wage                 , 0.012)
    , (17*min_wage,  lambda wage:     0.7*wage                 , 0.014)
    , (18*min_wage,  lambda wage:     0.7*wage                 , 0.016)
    , (19*min_wage,  lambda wage:     0.7*wage                 , 0.018)
    , (20*min_wage,  lambda wage: min(0.7*wage, 25*min_wage)   , 0.02) ]
  }

ss_contribs_by_employer = {
  # For employees, but not contractors, some contributions are also made by the employer.
  "pension" :
    [ ( 0,           lambda wage: 0                          , 0.0)
    , ( min_wage,    lambda wage: wage                       , 0.12)
    , ( 13*min_wage, lambda wage: min(0.7*wage, 25*min_wage) , 0.12) ]
  , "salud" :
    [ ( 0,           lambda wage: 0                          , 0.0)
    , ( 10*min_wage, lambda wage: wage                       , 0.085)
    , ( 13*min_wage, lambda wage: min(0.7*wage, 25*min_wage) , 0.085) ]
  , "parafiscales" :
    [ ( 0,           lambda wage: 0                          , 0.0 )
    , ( 10*min_wage, lambda wage: wage                       , 0.05 )
    , ( 13*min_wage, lambda wage: min(0.7*wage, 25*min_wage) , 0.05 ) ]
  , "cajas de compensacion" :
    [ ( 0,           lambda wage: 0                          , 0.0)
    , ( min_wage,    lambda wage: wage                       , 0.04)
    , ( 13*min_wage, lambda wage: min(0.7*wage, 25*min_wage) , 0.04) ]
  , "cesantias + primas":
    [ ( 0,           lambda wage: 0                          , 0.0)
    , ( min_wage,    lambda wage: wage                       , 2.12 / 12 )
      # Every year a worker gets 1 prima de servicio worth
      # 1 month's wages, and 1 cesantia worth 1.12 month's wages.
      # Summing those gives a yearly figure of 2.12.
      # Dividing by 12 amortizes it into a monthly one.
    , ( 13*min_wage, lambda wage: 0                          , 0.0 ) ]
  }