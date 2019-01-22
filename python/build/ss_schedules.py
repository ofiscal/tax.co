parafiscales = only for asalariados, and paid only by the employer
  and only for employees who earn more than 10 minimum wages

Minimum Wage 2016: COP$689454 
Minimum Wage 2017: COP$737717

In the data is the nominal salary, before those contributions.

salario integral: where they just give you money because you're making so much money. specifically 13 min wages. Here the employer expects you to pay your "prestaciones sociales", rather than the employer paying them. Prestaciones sociales = cesantias, "interest" (12% more) on cesantias, and prima de servicios = the biannual half-a-month's salary bonus.

First number: threshold
Second: taxable base
Third: rate

ss_contrib_schedules = {
  "pension" : {
    "contractor" : [
      (0, 0, 0.0) # if your (nominal, total) income is below the min wage, no contrib
      , ( minimum_wage
          , min(max(0.4*labor_income,minimum_wage)
                ,25*minimum_wage)
          , 0.16) ]
    , "employeeSchedule" : [
    # There's a discontinuity in the average tax rate when one's income crosses
    #  13 min wages. The average rate is 0.04 before, and 0.7 * 0.04 after.
      (0, 0 , 0.0)
      , (minimum_wage, labor_income, 0.04)
      , (13*minimum_wage
         , min(0.7*labor_income,25*minimum_wage), 0.04) ]
  } , "salud" :  {
    "contractor" : [
      (0, min(max(0.4*labor_income,minimum_wage),25*minimum_wage) , 0.125)
    ]
    , "employeeSchedule" : [
      (0, 0 , 0.0)
      , (minimum_wage, labor_income, 0.04)
      # This is another discrete fall in the average tax rate.
      , (13*minimum_wage, min(0.7*labor_income,25*minimum_wage), 0.04) ]
  } , "solidaridad" :  {
        "contractor" : [
          (0, 0, 0.0)
          , (4*minimum_wage
             ,min(max(0.4*labor_income,minimum_wage),25*minimum_wage),  0.01)
          , (16*minimum_wage
             , min(max(0.4*labor_income,minimum_wage),25*minimum_wage),0.012)
          , (17*minimum_wage
             , min(max(0.4*labor_income,minimum_wage),25*minimum_wage),0.014),
          (18*minimum_wage
           , min(max(0.4*labor_income,minimum_wage),25*minimum_wage),0.016),
          (19*minimum_wage
           , min(max(0.4*labor_income,minimum_wage),25*minimum_wage),0.018)
          (20*minimum_wage
           , min(max(0.4*labor_income,minimum_wage),25*minimum_wage),0.02)]
    , "employeeSchedule" : [
      (0, 0, 0.0)
      , (4*minimum_wage,labor_income,  0.01)
      , (13*minimum_wage,0.7*labor_income,  0.01)
      , (16*minimum_wage,0.7* labor_income,0.012)
      , (17*minimum_wage, 0.7*labor_income, 0.014),
      (18*minimum_wage, 0.7*labor_income,0.016),
      (19*minimum_wage, 0.7*labor_income,0.018)
      (20*minimum_wage, min(0.7*labor_income, 25*minimum_wage),0.02)]
      }
    }

# For employees, you also need the portion of the contributions that comes from the employer. The employer also contributes to Parafiscales, cajas de compensación and cesantías:

employer contributions: {
  # They only do this for asalariados.
  "pension" : { [ (0, 0, 0.0)
                , (minimum_wage, labor_income, 0.12)
                  , (13*minimum_wage, min(0.7*labor_income, 25*minimum_wage), 0.12) ] }
  , "salud" :  { [ (0,0,0.0)
                   , (10*minimum_wage, labor_income, 0.085)
                   , (13*minimum_wage, min(0.7*labor_income, 25*minimum_wage), 0.085) ] }
  , "parafiscales" : { [(0,0,0.0)
                        , (10*minimum_wage, labor_income, 0.05)
                        , (13*minimum_wage, min(0.7*labor_income, 25*minimum_wage), 0.05) ] }
  , "cajas de compensación" : {[
    (0,0,0.0)
    , (minimum_wage, labor_income, 0.04)
    , (13*minimum_wage, min(0.7*labor_income, 25*minimum_wage), 0.04) ] }
  , "cesantías": {
    (0,0,0.0)
    , (minimum_wage, labor_income, 2.12/12) # david will interpret
    , (13*minimum_wage, 0,0.0 ) } }
