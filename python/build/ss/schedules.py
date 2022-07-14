#####################################################
##### PITFALL: This code was defined using two idioms
#####################################################

"""Initially and for years, the SS schedules were defined as code.
That idiom did not lend itself well to the interactive online model,
for which users would like to define their own parameters.

To facilitate that, in 2022 I am refactoring the program using a new idiom,
such that SS schedules are represented as CSV files.

`./schedules_test.py` includes tests to ensure that the two idioms are equivalent.
"""


import os
import pandas as pd
from   typing import Callable, Dict, List, Tuple

from python.common.misc import min_wage


###########################################
##### Tabular representation: The new idiom
###########################################

def average_tax_function (
    fraction_of_wage      : float, # fraction of wage taxed
    min_base_in_min_wages : float, # minimum wage assumed
    max_base_in_min_wages : float  # maximum wage taxed
) -> Callable [ [float], float ]: # computes taxable base from wage
  return ( lambda wage:
           min ( max ( wage     * fraction_of_wage,
                       min_wage * min_base_in_min_wages ),
                 min_wage       * max_base_in_min_wages ) )

def ss_tax_schedule_from_frame (
    df : pd.DataFrame
) -> List [ Tuple [ float,                       # minimum income threshold
                    Callable [ [float], float ], # computes taxable base from wage
                    float ]]:                    # average (not marginal!) tax rate
  df["lambda"] = df.apply (
    lambda row: average_tax_function (
      row["fraction_of_wage"],
      row["min_base_in_min_wages"],
      row["max_base_in_min_wages"] ),
    axis = "columns" )
  df["min_threshold"] = df["min_threshold_in_min_wages"] * min_wage
  return ( df [[ "min_threshold",
                 "lambda",
                 "average_tax_rate" ]]
           . values . tolist () )

def ss_tax_schedule_from_csv (
    basename : str,
) -> List [ Tuple [ float,                       # minimum income threshold
                    Callable [ [float], float ], # computes taxable base from wage
                    float ] ]:                   # average (not marginal!) tax rate
  return ss_tax_schedule_from_frame (
    pd.read_csv (
      os.path.join ( "data/ss/",
                     basename + ".csv") ) )

ss_contrib_schedule_for_contractor_new : \
  Dict [ str,
         List [ Tuple [ float,                       # minimum income threshold
                        Callable [ [float], float ], # computes taxable base from wage
                        float ]                      # average (not marginal!) tax rate
               ] ] = \
  { "pension"     : ss_tax_schedule_from_csv ( "contractor_pension" ),
    "salud"       : ss_tax_schedule_from_csv ( "contractor_salud" ),
    "solidaridad" : ss_tax_schedule_from_csv ( "contractor_solidaridad" ), }

ss_contrib_schedule_for_employee_new : \
  Dict [ str,
         List [ Tuple [ float,                       # minimum income threshold
                        Callable [ [float], float ], # computes taxable base from wage
                        float ]                      # average (not marginal!) tax rate
               ] ] = \
  { "pension"     : ss_tax_schedule_from_csv ( "employee_pension" ),
    "salud"       : ss_tax_schedule_from_csv ( "employee_salud" ),
    "solidaridad" : ss_tax_schedule_from_csv ( "employee_solidaridad" ), }

# For employees, but not contractors,
# some contributions are also made by the employer.
ss_contribs_by_employer_new : \
  Dict [ str,
         List [ Tuple [ float,                       # minimum income threshold
                        Callable [ [float], float ], # computes taxable base from wage
                        float ]                      # average (not marginal!) tax rate
               ] ] = \
 { "pension"              : ss_tax_schedule_from_csv ( "employee_pension" ),
  "cajas de compensacion" : ss_tax_schedule_from_csv ( "employer_cajas_de_compensacion" ),
  "cesantias + primas"    : ss_tax_schedule_from_csv ( "employer_cesantias_y_primas" ),
  "parafiscales"          : ss_tax_schedule_from_csv ( "employer_parafiscales" ),
  "salud"                 : ss_tax_schedule_from_csv ( "employer_saluid" ), }


########################################
##### Code representation: The old idiom
########################################

ss_contrib_schedule_for_contractor : \
  Dict [ str,
         List [ Tuple [ float,                       # minimum income threshold
                        Callable [ [float], float ], # computes taxable base from wage
                        float ]                      # average (not marginal!) tax rate
               ] ] = \
  { "pension" :
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

ss_contrib_schedule_for_employee : \
  Dict [ str,
         List [ Tuple [ float,                       # minimum income threshold
                        Callable [ [float], float ], # computes taxable base from wage
                        float ]                      # average (not marginal!) tax rate
               ] ] = \
  { "pension" :
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

# For employees, but not contractors,
# some contributions are also made by the employer.
ss_contribs_by_employer : \
  Dict [ str,
         List [ Tuple [ float,                       # minimum income threshold
                        Callable [ [float], float ], # computes taxable base from wage
                        float ]                      # average (not marginal!) tax rate
               ] ] = \
  { "pension" :
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
