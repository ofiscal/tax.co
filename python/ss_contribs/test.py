# see rentas_naturales.xlsx for a model

import pandas as pd
import unittest


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

def ss_contribs(
  schedMapMap # a map from tax type (pension | salud | solidaridad) to
              # a map from whether the work is contract work ( 0 | 1 ) to
              # a schedule of marginal rates (see _accumulate_across_marginal_rates)
  , contractor # a column of 0-1 indicators of whether someone is a contractor
  , income ):  # a column of numbers
  def intToContractorKey(i):
    if   i == 1 : return "contractor"
    elif i == 0 : return "employee"
    else        : raise ValueError( "intToContractorKey should receive 0 or 1." )
  df = pd.DataFrame( [ income.copy()
                     , contractor.copy()
                   ] , index = ["income","contractor"]
                   ) . transpose()
  for tax_type in ss_contrib_schedules.keys():
    schedMap = schedMapMap[ tax_type ]
    for whether_contractor in [0,1]:
      sched = schedMap[ intToContractorKey( whether_contractor ) ]
      df.loc[       df["contractor"] == whether_contractor
                    , tax_type
            ] = df[ df["contractor"] == whether_contractor
                  ] [ "income"
                  ] . apply( lambda x: accumulate_across_marginal_rates( sched, x ) )
  return df[ list( ss_contrib_schedules.keys() ) ]

class Test_accumulate_across_marginal_rates(unittest.TestCase):
  def test_one_number(self):
    sched = [(0,0.1), (10,0.2)]
    self.assertEqual( accumulate_across_marginal_rates( sched, 1 )
                      , 0.1 )
    self.assertEqual( accumulate_across_marginal_rates( sched, 11 )
                      , 1.2 )
  def test_sample_data(self):
    ppl = pd.DataFrame(
      [ [ 0, 0   ]
      , [ 1, 1e6 ]
      , [ 0, 2e6 ]
      ] , columns = ["contractor","income"]
    )
    ss_contrib_schedules = {
      "pension" : {
        "contractor" : [ (0  , 0.0)
                       , (1e6, 0.1)
                       , (5e6, 0.2) ]
        , "employee" : [ (0  , 0.1)
                       , (1e6, 0.2)
                       , (5e6, 0.3) ]
      } , "salud" :  {
        "contractor" : [ (0  , 0.01)
                       , (1e6, 0.01)
                       , (5e6, 0.02) ]
        , "employee" : [ (0  , 0.01)
                       , (1e6, 0.02)
                       , (5e6, 0.03) ]
      } , "solidaridad" :  {
        "contractor" : [ (0  , 0.001)
                       , (1e6, 0.001)
                       , (5e6, 0.002) ]
        , "employee" : [ (0  , 0.001)
                       , (1e6, 0.002)
                       , (5e6, 0.003) ]
      }
    }
    self.assertTrue(
      (
        ss_contribs( ss_contrib_schedules, ppl["contractor"], ppl["income"] )
        == pd.DataFrame( [
            [ 0  , 0  , 0   ]
          , [ 0  , 1e4, 1e3 ]
          , [ 3e5, 3e4, 3e3 ]
          ] , columns = ["pension", "salud", "solidaridad"]
      ) ) . all() . all() )

def runTests():
  suite = unittest.TestSuite()
  suite.addTest(Test_accumulate_across_marginal_rates("test_one_number"))
  suite.addTest(Test_accumulate_across_marginal_rates("test_sample_data"))
  unittest . TextTestRunner() . run( suite )
