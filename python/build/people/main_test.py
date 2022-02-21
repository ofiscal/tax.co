###### see "remaining columns to test", below ######

if True:
  import numpy as np
  import pandas as pd
  #
  import python.build.classes as cla
  import python.build.output_io as oio
  import python.build.people.files as files
  import python.build.people.main_defs as defs
  import python.common.common as com
  from   python.common.misc import num_people
  import python.common.util as util


## unit tests

def test_count_num_matches_in_space_separated_list():
  assert 4 == ( defs.count_num_matches_in_space_separated_list
                ( " 1 2 3 1 2 3 ", {1,2} ) )
  assert 2 == ( defs.count_num_matches_in_space_separated_list
                ( " 11 2 3 11 2 3 ", {1,2} ) )
  assert 0 == ( defs.count_num_matches_in_space_separated_list
                ( "", {1,2} ) )


## integration tests

def test_ranges(ppl: pd.DataFrame):
  assert( util.unique( ppl.columns ) )
  specs = {
      "household"          : cla.InRange( 0, 1e7 )
    , "age"                : cla.InRange( 0, 120 )
    , "edu"                : cla.InSet( set( files.edu_key.values() ) )
    , "female"             : cla.InRange( 0, 1 )
    , "household-member"   : cla.InRange( 1, 50 )
    , "income, pension"    : cla.InRange( 0, 3e8 )
    , "income, cesantia"   : cla.InRange( 0, 1e8 )
    , "income, dividend"   : cla.InRange( 0, 1e8 )
    , "independiente"      : cla.InRange( 0, 1 )
    , "literate"           : cla.InRange( 0, 1 )
    , "student"            : cla.InRange( 0, 1 )
    , "weight"             : cla.InRange( 0.001, 1e4 )
    , "pension, contributing (if not pensioned)"
                           : cla.InRange(0,1)
    , "pension, receiving" : cla.InRange(0,1)
    , "pension, contributor(s) (if not pensioned) = split"
                           : cla.InRange(0,1)
    , "pension, contributor(s) (if not pensioned) = self"
                           : cla.InRange(0,1)
    , "pension, contributor(s) (if not pensioned) = employer"
                           : cla.InRange(0,1)
    , "seguro de riesgos laborales"             : cla.InRange(0, 1)
    , "income, govt, cash"                      : cla.InRange(0, 2e7)
    , "income, govt, in-kind"                   : cla.InRange(0, 1e7)
    , "income, non-labor (tax def)"             : cla.InRange(0, 1e8)
    , "income, rental + interest"               : cla.InRange(0, 1e9)
    , "income, donacion"                        : cla.InRange(0, 2e7)
    , "income, infrequent"                      : cla.InRange(0, 1e8)
    , "income, ganancia ocasional, 10%-taxable" : cla.InRange(0, 1e8)
    , "income, ganancia ocasional, 20%-taxable" : cla.InRange(0, 3e7)
    , "income, labor, cash"                     : cla.InRange(0, 3e9)
    , "income, labor, in-kind"                  : cla.InRange(0, 3e7)
    , "income, cash"                            : cla.InRange(0, 3e9)
    , "income, in-kind"                         : cla.InRange(0, 3e7)
    , "income"                                  : cla.InRange(0, 3e9)
    , "income, govt"                            : cla.InRange(0, 3e7)
    , "income, private"                         : cla.InRange(0, 2e8)
    , "income, labor"                           : cla.InRange(0, 3e9)
    , "income, borrowing"                       : cla.InRange(0, 1e8)
    , "rank, labor income"                      : cla.InRange(1, 50)
    , "empleado"                                : cla.InRange(0,1)
    , "desempleado"                             : cla.InRange(0,1)
    , "in labor force"                          : cla.InRange(0,1)
    , "used savings"   : cla.InSet( {True,False} )
    , "disabled"       : cla.InSet( {True,False} )
    , "dependent"      : cla.InSet( {True,False} )
    , "race, indig"    : cla.InSet( {True,False} )
    , "race, git|rom"  : cla.InSet( {True,False} )
    , "race, raizal"   : cla.InSet( {True,False} )
    , "race, palenq"   : cla.InSet( {True,False} )
    , "race, neg|mul"  : cla.InSet( {True,False} )
    , "race, whi|mest" : cla.InSet( {True,False} ) }
  for k in specs.keys():
    assert specs[k] . test( ppl[k] )

# TODO ! Test that all other variables are missing nothing.
def test_upper_bound_on_fraction_missing(ppl: pd.DataFrame):
  specs = { # test_ranges guarantees that these are
            # the only columns with missing values
      "literate"                                              : 0.15
    , "student"                                               : 0.15
    , "pension, contributing (if not pensioned)"              : 0.7
    , "pension, contributor(s) (if not pensioned) = split"    : 0.9
    , "pension, contributor(s) (if not pensioned) = self"     : 0.9
    , "pension, contributor(s) (if not pensioned) = employer" : 0.9
    , "seguro de riesgos laborales"                           : 0.7

    , "empleado"                                              : 0
    , "desempleado"                                           : 0
    , "in labor force"                                        : 0
    }
  for k in specs.keys():
    assert (pd.isnull(ppl[k]).sum() / len(ppl)) <= specs[k]

# TODO : extend to all the old variables
def test_means( ppl : pd.DataFrame ) -> None:
  for (col, theMin, theMax) in [
      ("used savings"   , 0.005, 0.05),
      ("empleado"       , 0.20,  0.6),
      ("desempleado"    , 0.03,  0.12),
      ("in labor force" , 0.25,  0.6),  ]:
    x = ppl[col].mean()
    assert (x >= theMin ) & (x <= theMax)


if True: # run tests
  log = "starting\n"

  # unit tests
  test_count_num_matches_in_space_separated_list()

  # integration tests
  ppl = oio.readStage(com.subsample, 'people_1')
  ppl["edu"] = util.interpretCategorical( ppl["edu"]
                                              , files.edu_key.values() )
  test_ranges( ppl )
  test_upper_bound_on_fraction_missing( ppl )
  test_means( ppl )

  assert util.near( len(ppl),
                    num_people / com.subsample,
                    tol_frac = 1/5 )

  oio.test_write( com.subsample
                , "people_main"
                , log )
