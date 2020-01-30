# PURPOSE
#########
# These functions return triples that encode how to
# determine someone's income tax as a function of their wage.
# Interpret those triples as follows:
    # First number: threshold at which a new income tax rate takes effect.
    # Second: taxable base. This is a function; you input someone's wage,
    #   and it outputs the amount of their money subject to the tax.
    # Third: average tax rate.

# PITFALL
#########
# The ENPH data gives nominal salary, before those contributions.

# PITFALL
#########
# Contractors pay all income taxes themselves. Employees do not --
# they pay some part of those taxes themselves,
# and their employer pays the rest.
# (In an economic sense, it all comes out of the employee's wages,
# but in a legal sense, it is shared with the employer.)

# CONTEXT
#########
# The model `rentas_naturales.xlsx` might amke this easier to understand.

from python.common.misc import min_wage

ss_contrib_schedule_for_contractor = {
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
    , ( 13*min_wage, lambda wage: 0                          , 0.0 ) ]
  }
