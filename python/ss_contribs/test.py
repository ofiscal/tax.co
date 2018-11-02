# see rentas_naturales.xlsx for a model

import pandas as pd
import unittest

ppl = pd.DataFrame(
  [ [ 0, 0 ]
  , [ 1, 10e5 ]
  , [ 1, 10e6 ]
  , [ 1, 10e7 ]
  , [ 0, 10e5 ]
  , [ 0, 10e6 ]
  , [ 0, 10e7 ]
  ] , columns = ["contractor","income"]
)

ss_contrib_schedules = {
  "pension" : {
    "contractor" : [ (0  , 0.0)
                   , (1e6, 0.1)
                   , (5e6, 0.2) ]
    , "employeeSchedule" : [ (0  , 0.1)
                           , (1e6, 0.2)
                           , (5e6, 0.3) ]
  } , "salud" :  {
    "contractor" : [ (0  , 0.01)
                   , (1e6, 0.01)
                   , (5e6, 0.02) ]
    , "employeeSchedule" : [ (0  , 0.01)
                           , (1e6, 0.02)
                           , (5e6, 0.03) ]
  }
}

def accumulate_across_marginal_rates( sched, income ):
  return _accumulate_across_marginal_rates( sched, income, 0, 0 )

def _accumulate_across_marginal_rates(
    sched # a list of (threshold, marginal rate) pairs, ordered on threshold
          # starting at threshold = 0
    , income # a number, total income
    , taxed # a number, income already taxed at earlier rates
    , acc ): # a number, tax already accumulated at earlier rates
  (thresh, rate) = sched[0]
  if len( sched ) == 1:
    payOn = income - taxed
  else: # len( sched ) should never be less than 1
    (threshNext,_) = sched[1]
    payOn = min( threshNext, income ) - taxed
  acc = acc + payOn * rate
  if len( sched ) == 1: return acc
  else:
    if income <= threshNext: return acc
    else: return _accumulate_across_marginal_rates(
                 sched[1:], income, threshNext, acc )

class Tests(unittest.TestCase):
  def test_accumulate_across_marginal_rates(self):
    sched = [(0,0.1), (10,0.2)]
    self.assertEqual( accumulate_across_marginal_rates( sched, 1 )
                      , 0.1 )
    self.assertEqual( accumulate_across_marginal_rates( sched, 11 )
                      , 1.2 )

try: unittest.main()
except SystemExit: pass
