# TODO: Use CSV files to represent SS contribution schedules,
# as begun in ./csv_paused/.

import os
import pandas as pd
from   typing import Callable, Dict, List, Tuple
#
from   python.common.misc import min_wage
from   python.build.ss.types import AverageTaxSchedule


ss_contrib_schedule_for_contractor : \
  Dict [ str, AverageTaxSchedule ] = {
    # PITFALL: cajas de compensacion : voluntary => 0 contributions.
    # That is, since the microsimulation computes what someone *must* legally pay,
    # not what they actually pay, and since contributions to cajas de compensacion
    # are voluntary, we have made them 0 for contractors by omitting that category here.
    "ARL" :
    [ ( 0, lambda _: 0, 0.0 )
    , ( min_wage,
        lambda wage: min( max( 0.4*wage, min_wage ),
                          25*min_wage )
      , 0.00522 ) ] # PITfALL: This is the minimum. The true value is complex.
  , "pension" :
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
  { # PITFALL: Suponemos que un dependiente
    # que gana menos de un salario mínimo
    # trabaje por horas, según el decreto 2616 de 2013.
    "pension" :
    [ ( 0,                lambda wage: 0                          , 0.0 )
    , ( 3, # PITFALL: Literally 3 COP per month.
           # This is to effectively create a 0-income bracket, where contributions are 0.
           # The reason I chose 3 COP is that it is basically nothing,
           # but greater than the 2 COP theoretical maximum that a zero-income household
           # might "earn" in the microsimulation after I've twice added a random amount
           # between 0 and 1 peso, in order to make the quantiles well-defined.
                              lambda wage:     min_wage / 4           , 0.04)
    , (     min_wage / 4 + 1, lambda wage: 2 * min_wage / 4           , 0.04)
    , ( 2 * min_wage / 4 + 1, lambda wage: 3 * min_wage / 4           , 0.04)
    , ( 3 * min_wage / 4 + 1, lambda wage:     min_wage               , 0.04)
      # PITFALL: The reason the above three lines add 1 COP
      # to the threshold (n/4) * min_wage (for n in [1,2,3])
      # is that if you make exactly n/4 minimum wages,
      # you pay the same rate as
      # someone who earns slightly less than that threshold.
      #
      # COMMENT NAME: "Raising low pension thresholds by 1 COP".
    , ( min_wage,             lambda wage:         wage               , 0.04)
    , ( 13*min_wage,          lambda wage: min(0.7*wage, 25*min_wage) , 0.04) ]
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
  { "ARL" : # Admin. de Riesgos Laborales
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
  , "cesantias + primas":
    [ ( 0,           lambda wage: min_wage                   , 2.12 / 12 )
    , ( min_wage,    lambda wage: wage                       , 2.12 / 12 )
      # Every year a worker gets 1 prima de servicio worth
      # 1 month's wages, and 1 cesantia worth 1.12 month's wages.
      # Summing those gives a yearly figure of 2.12.
      # Dividing by 12 amortizes it into a monthly one.
      # Thus this is income, albeit strangely distributed over time.
    , ( 13*min_wage, lambda wage: 0                          , 0.0 ) ]
  , "parafiscales" : # This is ICBF + SENA
    [ ( 0,           lambda wage: 0                          , 0.0 )
    , ( 10*min_wage, lambda wage: wage                       , 0.05 )
    , ( 13*min_wage, lambda wage: min(0.7*wage, 25*min_wage) , 0.05 ) ]
  , "pension" :
    [ ( 0,                    lambda wage: 0                          , 0.0 )
    , ( 3,                    lambda wage:     min_wage / 4           , 0.12)
    , (     min_wage / 4 + 1, lambda wage: 2 * min_wage / 4           , 0.12)
    , ( 2 * min_wage / 4 + 1, lambda wage: 3 * min_wage / 4           , 0.12)
    , ( 3 * min_wage / 4 + 1, lambda wage:     min_wage               , 0.12)
      # PITFALL: The reason the above three lines add 1 COP
      # is documented above in the comment labeled
      # COMMENT NAME: "Raising low pension thresholds by 1 COP".
    , ( min_wage,             lambda wage: wage                       , 0.12)
    , ( 13*min_wage,          lambda wage: min(0.7*wage, 25*min_wage) , 0.12) ]
  , "salud" :
    [ ( 0,           lambda wage: 0                          , 0.0)
    , ( 10*min_wage, lambda wage: wage                       , 0.085)
    , ( 13*min_wage, lambda wage: min(0.7*wage, 25*min_wage) , 0.085) ]
  , "vacaciones" : # Like cesantías, these are income.
    [ ( 0,           lambda wage: min_wage                   , 0.0417 )
    , ( min_wage,    lambda wage: wage                       , 0.0417 )
    , ( 13*min_wage, lambda wage: min(0.7*wage, 25*min_wage) , 0.0417 ) ]
  }
