# see rentas_naturales.xlsx for a model

import python.build.common as c


# How to interpret these triples:
    # First number: threshold at which the regime starts
    # Second: taxable base
    # Third: average tax rate
    # The data gives nominal salary, before those contributions.

ss_contrib_schedule_for_contractor = {
  "pension" :
    [ ( 0, lambda labor_income: 0, 0.0 )
    , ( c.min_wage
      , lambda labor_income: min( max( 0.4*labor_income, c.min_wage )
                                , 25*c.min_wage)
      , 0.16 ) ]
  , "salud" :
    [ ( 0
      , lambda labor_income: min( max( 0.4*labor_income, c.min_wage )
                                , 25*c.min_wage )
      , 0.125 ) ]
  , "solidaridad" :
    [ (0, lambda labor_income: 0, 0.0)
    , ( 4*c.min_wage
      , lambda labor_income: min( max(0.4*labor_income,c.min_wage)
                                , 25*c.min_wage)
      , 0.01)
    , ( 16*c.min_wage
      , lambda labor_income: min( max(0.4*labor_income,c.min_wage)
                                , 25*c.min_wage)
      , 0.012)
    , ( 17*c.min_wage
      , lambda labor_income: min( max(0.4*labor_income,c.min_wage)
                                , 25*c.min_wage)
      , 0.014)
    , ( 18*c.min_wage
      , lambda labor_income: min( max(0.4*labor_income,c.min_wage)
                                , 25*c.min_wage)
      , 0.016)
    , ( 19*c.min_wage
      , lambda labor_income: min( max(0.4*labor_income,c.min_wage)
                                , 25*c.min_wage)
      , 0.018)
    , ( 20*c.min_wage
      , lambda labor_income: min( max(0.4*labor_income,c.min_wage)
                                , 25*c.min_wage)
      , 0.02) ]
  }

ss_contrib_schedule_for_employee = {
  "pension" :
    [ ( 0,             lambda labor_income: 0                                      , 0.0)
    , ( c.min_wage,    lambda labor_income: labor_income                           , 0.04)
    , ( 13*c.min_wage, lambda labor_income: min( 0.7*labor_income, 25*c.min_wage)  , 0.04 ) ]
  , "salud" :
    [ ( 0,             lambda labor_income: 0                                      , 0.0 )
    , ( c.min_wage,    lambda labor_income: labor_income                           , 0.04 )
    , ( 13*c.min_wage, lambda labor_income: min( 0.7*labor_income, 25*c.min_wage ) , 0.04 ) ]
  , "solidaridad" :
    [ (0,              lambda labor_income: 0                                      , 0.0)
    , (4*c.min_wage,   lambda labor_income:     labor_income                       , 0.01)
    , (13*c.min_wage,  lambda labor_income: 0.7*labor_income                       , 0.01)
    , (16*c.min_wage,  lambda labor_income: 0.7*labor_income                       , 0.012)
    , (17*c.min_wage,  lambda labor_income: 0.7*labor_income                       , 0.014)
    , (18*c.min_wage,  lambda labor_income: 0.7*labor_income                       , 0.016)
    , (19*c.min_wage,  lambda labor_income: 0.7*labor_income                       , 0.018)
    , (20*c.min_wage,  lambda labor_income: min(0.7*labor_income, 25*c.min_wage)   , 0.02) ]
  }

ss_contribs_by_employers = {
  # For employees, but not contractors, some contributions are also made by the employer.
  "pension" :
    [ ( 0,             lambda labor_income: 0                                    , 0.0)
    , ( c.min_wage,    lambda labor_income: labor_income                         , 0.12)
    , ( 13*c.min_wage, lambda labor_income: min(0.7*labor_income, 25*c.min_wage) , 0.12) ]
  , "salud" :
    [ ( 0,             lambda labor_income: 0                                    , 0.0)
    , ( 10*c.min_wage, lambda labor_income: labor_income                         , 0.085)
    , ( 13*c.min_wage, lambda labor_income: min(0.7*labor_income, 25*c.min_wage) , 0.085) ]
  , "parafiscales" :
    [ ( 0,             lambda labor_income: 0                                    , 0.0 )
    , ( 10*c.min_wage, lambda labor_income: labor_income                         , 0.05 )
    , ( 13*c.min_wage, lambda labor_income: min(0.7*labor_income, 25*c.min_wage) , 0.05 ) ]
  , "cajas de compensación" :
    [ ( 0,             lambda labor_income: 0                                    , 0.0)
    , ( c.min_wage,    lambda labor_income: labor_income                         , 0.04)
    , ( 13*c.min_wage, lambda labor_income: min(0.7*labor_income, 25*c.min_wage) , 0.04) ]
  , "cesantías":
    [ ( 0,             lambda labor_income: 0                                    , 0.0)
    , ( c.min_wage,    lambda labor_income: labor_income, 2.12 / 12 )
      # Every year a worker gets 1 prima de servicio worth 1 month's wages,
      # and 1 cesantia worth 1.12 month's wages. This formula gives the portion of
      # yearly income contributed each month to those.
    , ( 13*c.min_wage, lambda labor_income: 0                                    , 0.0 ) ]
  }
