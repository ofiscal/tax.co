# see rentas_naturales.xlsx for a model

from python.build.common import min_wage

# How to interpret these triples:
    # First number: threshold at which the regime starts
    # Second: taxable base
    # Third: average tax rate
    # The data gives nominal salary, before those contributions.

ss_contrib_schedule_for_contractor = {
  "pension" :
    [ ( 0, lambda wage: 0, 0.0 )
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
    [ (0,            lambda wage: 0                            , 0.0)
    , (4*min_wage,   lambda wage:     wage                     , 0.01)
    , (13*min_wage,  lambda wage: 0.7*wage                     , 0.01)
    , (16*min_wage,  lambda wage: 0.7*wage                     , 0.012)
    , (17*min_wage,  lambda wage: 0.7*wage                     , 0.014)
    , (18*min_wage,  lambda wage: 0.7*wage                     , 0.016)
    , (19*min_wage,  lambda wage: 0.7*wage                     , 0.018)
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
    , ( 10*min_wage, lambda wage: wage                       , 0.04)
    , ( 13*min_wage, lambda wage: min(0.7*wage, 25*min_wage) , 0.04) ]
  , "cesantias":
    [ ( 0,           lambda wage: 0                          , 0.0)
    , ( min_wage,    lambda wage: wage, 2.12 / 12 )
                 # Every year a worker gets 1 prima de servicio worth
                 # 1 month's wages, and 1 cesantia worth 1.12 month's wages.
    , ( 13*min_wage, lambda wage: 0                          , 0.0 ) ]
  }
