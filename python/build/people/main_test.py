###### see "remaining columns to test", below ######

import numpy as np
import pandas as pd
import re as regex

import python.build.classes as cla
import python.build.output_io as oio
import python.build.people.files as files
import python.common.cl_args as cl
import python.common.misc as c
import python.common.util as util


if True: # initialize log
  test_output_filename = "people_main"
  oio.test_clear( cl.subsample
                , test_output_filename )
  def echo( content ):
    oio.test_write( cl.subsample
                  , test_output_filename
                  , content )
  echo( ["starting"] )


def test_ranges(ppl: pd.DataFrame):
  specs = {
      "household"          : { cla.InRange( 0, 1e7 ) }
    , "age"                : { cla.InRange( 0, 120 ) }
    , "education"          : { cla.InSet( set( files.edu_key.values() ) ) }
    , "female"             : { cla.InRange( 0, 1 ) }
    , "household-member"   : { cla.InRange( 1, 50 ) }
    , "income, pension"    : { cla.InRange( 0, 3e8 ) }
    , "income, cesantia"   : { cla.InRange( 0, 1e8 ) }
    , "income, dividend"   : { cla.InRange( 0, 1e8 ) }
    , "independiente"      : { cla.InRange( 0, 1 ) }
    , "literate"           : { cla.InRange( 0, 1 ), cla.IsNull() }
    , "student"            : { cla.InRange( 0, 1 ), cla.IsNull() }
    , "weight"             : { cla.InRange( 0.001, 1e4 ) }
    , "pension, contributing (if not pensioned)"
                           : { cla.InRange(0,1),    cla.IsNull() }
    , "pension, receiving" : { cla.InRange(0,1) }
    , "pension, contributor(s) (if not pensioned) = split"
                           : { cla.InRange(0,1),    cla.IsNull() }
    , "pension, contributor(s) (if not pensioned) = self"
                           : { cla.InRange(0,1),    cla.IsNull() }
    , "pension, contributor(s) (if not pensioned) = employer"
                           : { cla.InRange(0,1),    cla.IsNull() }
    , "seguro de riesgos laborales"
                           : { cla.InRange(0, 1),   cla.IsNull() }
    , "income, govt, cash"                      : { cla.InRange(0, 2e7) }
    , "income, govt, in-kind"                   : { cla.InRange(0, 1e7) }
    , "income, non-labor"                       : { cla.InRange(0, 1e8) }
    , "income, capital (tax def)"               : { cla.InRange(0, 1e9) }
    , "income, donacion"                        : { cla.InRange(0, 2e7) }
    , "income, infrequent"                      : { cla.InRange(0, 1e8) }
    , "income, ganancia ocasional, 10%-taxable" : { cla.InRange(0, 1e8) }
    , "income, ganancia ocasional, 20%-taxable" : { cla.InRange(0, 3e7) }
    , "income, labor, cash"                     : { cla.InRange(0, 3e9) }
    , "income, labor, in-kind"                  : { cla.InRange(0, 3e7) }
    , "income, cash"                            : { cla.InRange(0, 3e9) }
    , "income, in-kind"                         : { cla.InRange(0, 3e7) }
    , "income"                                  : { cla.InRange(0, 3e9) }
    , "income, govt"                            : { cla.InRange(0, 3e7) }
    , "income, private"                         : { cla.InRange(0, 2e8) }
    , "income, labor"                           : { cla.InRange(0, 3e9) }
    , "income, borrowing"                       : { cla.InRange(0, 1e8) }
    , "member-by-income"                        : { cla.InRange(1, 50) }
    , "disabled"       : { cla.InSet( {True,False} ) }
    , "dependent"      : { cla.InSet( {True,False} ) }
    , "race, indig"    : { cla.InSet( {True,False} ) }
    , "race, git|rom"  : { cla.InSet( {True,False} ) }
    , "race, raizal"   : { cla.InSet( {True,False} ) }
    , "race, palenq"   : { cla.InSet( {True,False} ) }
    , "race, neg|mul"  : { cla.InSet( {True,False} ) }
    , "race, whi|mest" : { cla.InSet( {True,False} ) } }
  for k in specs.keys():
    assert cla.properties_cover_num_column( specs[k], ppl[k] )

def test_upper_bound_on_fraction_missing(ppl: pd.DataFrame):
  specs = { # test_ranges guarantees that these are
            # the only columns with missing values
      "literate"                                              : 0.1
    , "student"                                               : 0.1
    , "pension, contributing (if not pensioned)"              : 0.7
    , "pension, contributor(s) (if not pensioned) = split"    : 0.9
    , "pension, contributor(s) (if not pensioned) = self"     : 0.9
    , "pension, contributor(s) (if not pensioned) = employer" : 0.9
    , "seguro de riesgos laborales"                           : 0.7
    }
  for k in specs.keys():
    assert (pd.isnull(ppl[k]).sum() / len(ppl)) < specs[k]

if True: # run tests
  # build data
  ppl = oio.readStage(cl.subsample, 'people_1')
  ppl["education"] = util.interpretCategorical( ppl["education"]
                                              , files.edu_key.values() )

  # integration test
  test_ranges( ppl )
  test_upper_bound_on_fraction_missing( ppl )
