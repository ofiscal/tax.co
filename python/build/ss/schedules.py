#####################################################
##### PITFALL: This code was defined using two idioms
##### The new idiom, however, never took effect.
#####################################################

"""Initially and for years, the SS schedules were defined as code.
That idiom did not lend itself well to the interactive online model,
for which users would like to define their own parameters.

To facilitate that,
in 2022 I started refactoring the program using a new idiom,
such that SS schedules are represented as CSV files.

`./schedules_test.py` includes tests to ensure that the two idioms are equivalent.

Our priorities then changed, and I have not finished the conversion.
"""

import os
import pandas as pd
from   typing import Callable, Dict, List, Tuple
#
from   python.common.misc import min_wage
from   python.build.ss.types import AverageTaxSchedule


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
) ->  AverageTaxSchedule:
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
) -> AverageTaxSchedule:
  return ss_tax_schedule_from_frame (
    pd.read_csv (
      os.path.join ( "data/ss/",
                     basename + ".csv") ) )

ss_contrib_schedule_for_contractor_new : \
  Dict [ str, AverageTaxSchedule ] = {
    "pension"     : ss_tax_schedule_from_csv ( "contractor_pension"     ),
    "salud"       : ss_tax_schedule_from_csv ( "contractor_salud"       ),
    "solidaridad" : ss_tax_schedule_from_csv ( "contractor_solidaridad" ), }

ss_contrib_schedule_for_employee_new : \
  Dict [ str, AverageTaxSchedule ] = {
    "pension"     : ss_tax_schedule_from_csv ( "employee_pension"     ),
    "salud"       : ss_tax_schedule_from_csv ( "employee_salud"       ),
    "solidaridad" : ss_tax_schedule_from_csv ( "employee_solidaridad" ), }

# For employees, but not contractors,
# some contributions are also made by the employer.
ss_contribs_by_employer_new : \
  Dict [ str, AverageTaxSchedule ] = {
    "pension"               : ss_tax_schedule_from_csv ( "employer_pension"               ),
    "cajas de compensacion" : ss_tax_schedule_from_csv ( "employer_cajas_de_compensacion" ),
    "cesantias + primas"    : ss_tax_schedule_from_csv ( "employer_cesantias_y_primas"    ),
    "parafiscales"          : ss_tax_schedule_from_csv ( "employer_parafiscales"          ),
    "salud"                 : ss_tax_schedule_from_csv ( "employer_saluid"                ), }


########################################
##### Code representation: The old idiom
########################################

ss_contrib_schedule_for_contractor : \
  Dict [ str, AverageTaxSchedule ] = {
    # PITFALL: cajas de compensacion : voluntary => 0 contributions.
    # That is, since the microsimulation computes what someone *must* legally pay,
    # not what they actually pay, and since contributions to cajas de compensacion
    # are voluntary, we have made them 0 for contractors by omitting that category here.
    "pension" :
    [ ( 0, lambda _: 0, 0.0 )
    , ( min_wage
      , lambda wage: min( max( 0.4*wage, min_wage ),
                          25*min_wage)
      , 0.16 ) ]
  , "salud" :
    [ ( 0, lambda _: 0, 0.0 ),
      ( min_wage,
        lambda wage: min( max( 0.4*wage, min_wage ),
                          25*min_wage ),
        0.125 ) ]
  , "ARL" :
    [ ( 0, lambda _: 0, 0.0 )
    , ( min_wage,
        lambda wage: min( max( 0.4*wage, min_wage ),
                          25*min_wage )
      , 0.00522 ) ] # PITfALL: This is the minimum. The true value is complex.
  , "solidaridad" :
    [ (0, lambda wage: 0, 0.0)
    , ( 4*min_wage
      , lambda wage: min( max(0.4*wage,min_wage),
                          25*min_wage)
      , 0.01)
    , ( 16*min_wage
      , lambda wage: min( max(0.4*wage,min_wage),
                          25*min_wage)
      , 0.012)
    , ( 17*min_wage
      , lambda wage: min( max(0.4*wage,min_wage),
                          25*min_wage)
      , 0.014)
    , ( 18*min_wage
      , lambda wage: min( max(0.4*wage,min_wage),
                          25*min_wage)
      , 0.016)
    , ( 19*min_wage
      , lambda wage: min( max(0.4*wage,min_wage),
                          25*min_wage)
      , 0.018)
    , ( 20*min_wage
      , lambda wage: min( max(0.4*wage,min_wage),
                          25*min_wage)
      , 0.02) ]
  }

ss_contrib_schedule_for_employee : \
  Dict [ str, AverageTaxSchedule ] = \
  { # PITFALL: Suponemos que un dependiente que gane menos de un salario minimo
    # trabaja por horas segun el decreto 2616 de 2013.
    "pension" :
    [ ( 0,                lambda wage: 0                          , 0.0 )
    , ( 3, # PITFALL: Literally 3 COP per month.
           # This is to effectively create a 0-income bracket, where contributions are 0.
           # The reason I chose 3 COP is that it is basically nothing,
           # but greater than the 2 COP theoretical maximum that a zero-income household
           # might "earn" in the microsimulation after I've twice added a random amount
           # between 0 and 1 peso, in order to make the quantiles well-defined.
                          lambda wage:     min_wage / 4           , 0.04)
    , (     min_wage / 4, lambda wage: 2 * min_wage / 4           , 0.04)
    , ( 2 * min_wage / 4, lambda wage: 3 * min_wage / 4           , 0.04)
    , ( 3 * min_wage / 4, lambda wage:     min_wage               , 0.04)
    , ( min_wage,         lambda wage:         wage               , 0.04)
    , ( 13*min_wage,      lambda wage: min(0.7*wage, 25*min_wage) , 0.04) ]
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
ss_contribs_by_employer :            \
  Dict [ str, AverageTaxSchedule ] = \
  { "pension" :
    [ ( 0,                lambda wage: 0                          , 0.0 )
    , ( 3,                lambda wage:     min_wage / 4           , 0.12)
    , (     min_wage / 4, lambda wage: 2 * min_wage / 4           , 0.12)
    , ( 2 * min_wage / 4, lambda wage: 3 * min_wage / 4           , 0.12)
    , ( 3 * min_wage / 4, lambda wage:     min_wage               , 0.12)
    , ( min_wage,         lambda wage: wage                       , 0.12)
    , ( 13*min_wage,      lambda wage: min(0.7*wage, 25*min_wage) , 0.12) ]
  , "salud" :
    [ ( 0,           lambda wage: 0                          , 0.0)
    , ( 10*min_wage, lambda wage: wage                       , 0.085)
    , ( 13*min_wage, lambda wage: min(0.7*wage, 25*min_wage) , 0.085) ]
  , "parafiscales" : # This is ICBF + SENA
    [ ( 0,           lambda wage: 0                          , 0.0 )
    , ( 10*min_wage, lambda wage: wage                       , 0.05 )
    , ( 13*min_wage, lambda wage: min(0.7*wage, 25*min_wage) , 0.05 ) ]
  , "ARL" :
    [ ( 0,           lambda _: min_wage                        , 0.00522 )
    , ( min_wage,    lambda wage: wage                         , 0.00522 )
    , ( 13*min_wage, lambda wage: min( 0.7*wage, 25*min_wage ) , 0.00522 ) ]
  , "aux transporte" :
    [ ( 0,           lambda _: 0                                , 0    )
    , ( # PITFALL: We derived this 0.1212069 value ourselves.
        # Auxilio de transporte is a fixed amount,
        # not one that depends on your wage,
        # given to people earning between 1 and 2 minima.
        # 0.1212069 = the aux amount in 2023 / the minimum wage in 2023.
        min_wage,    lambda wage: min_wage                      , 0.1212069 )
    , ( 2*min_wage,  lambda wage: 0                             , 0    ) ]
  , "cajas de compensacion" :
    [ ( 0,           lambda wage: min_wage                   , 0.04)
    , ( min_wage,    lambda wage: wage                       , 0.04)
    , ( 13*min_wage, lambda wage: min(0.7*wage, 25*min_wage) , 0.04) ]
  , "vacaciones" : # Like cesantías, this goes to the worker.
    [ ( 0,           lambda wage: min_wage                   , 0.0417 )
    , ( min_wage,    lambda wage: wage                       , 0.0417 )
    , ( 13*min_wage, lambda wage: min(0.7*wage, 25*min_wage) , 0.0417 ) ]
  , "cesantias + primas":
    [ ( 0,           lambda wage: min_wage                   , 2.12 / 12 )
    , ( min_wage,    lambda wage: wage                       , 2.12 / 12 )
      # Every year a worker gets 1 prima de servicio worth
      # 1 month's wages, and 1 cesantia worth 1.12 month's wages.
      # Summing those gives a yearly figure of 2.12.
      # Dividing by 12 amortizes it into a monthly one.
    , ( 13*min_wage, lambda wage: 0                          , 0.0 ) ]
  }
