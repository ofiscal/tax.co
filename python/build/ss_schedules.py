# PURPOSE
#########
# These functions return triples that encode how to
# determine someone's income tax as a function of their wage.
# Interpret those triples as follows:
    # First number: threshold at which a new income tax rate takes effect.
    # Second: taxable base. This is a function; you input someone's wage,
    #   and it outputs the amount of that money subject to the tax.
    # Third: average tax rate.

# PITFALL
#########
# The ENPH data gives nominal salary, before any of these contributions.

# PITFALL
#########
# Contractors pay all income taxes themselves. Employees do not --
# they pay some part of those taxes themselves,
# and their employer pays the rest.
# (In an economic sense, it all comes out of the employee's wages,
# but in a legal sense, the burden is shared with the employer.)

# CONTEXT
#########
# The model `rentas_naturales.xlsx` might make this easier to understand.

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


#### #### #### #### #### ####
#### Tests
#### TODO: Move to a separate file
#### #### #### #### #### ####

pension_contractor_frame = pd.DataFrame (
  { "min_threshold_in_min_wages" : [0    , 1   ],
    "fraction_of_wage"           : [0    , 0.4 ],
    "min_base_in_min_wages"      : [-9e99, 1   ],
    "max_base_in_min_wages"      : [9e99 , 25  ],
    "average_tax_rate"           : [0    , 0.16], } )

pension_contractor_schedule_from_frame = ss_tax_schedule_from_frame (
  df = pension_contractor_frame )

x = ss_contrib_schedule_for_contractor ["pension"]
y = ss_contrib_schedule_for_contractor ["pension"] [0]
z = ss_contrib_schedule_for_contractor ["pension"] [0] [0]


for b in [0,1]: # tax bracket
  for i in [0,2]: # list index
    assert ( pension_contractor_schedule_from_frame         [0][i] ==
             ss_contrib_schedule_for_contractor ["pension"] [0][i] )

  for w in range(25): # wage
    assert ( pension_contractor_schedule_from_frame         [0][1] (w) ==
             ss_contrib_schedule_for_contractor ["pension"] [0][1] (w) )

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
