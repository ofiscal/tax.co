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
  oio.test_clear( test_output_filename )
  def echo( content ):
    oio.test_write( test_output_filename
                  , content )
  echo( ["starting"] )


def test_people(ppl: pd.DataFrame):
  specs = {
    "household"   : { cla.InRange( 0, 1e7 ) }
    , "age"       : { cla.InRange( 0, 120 ) }
    , "education" : { cla.InSet( set( files.edu_key.values() ) ) }
    }
  for k in specs.keys():
    assert cla.properties_cover_num_column( specs[k], ppl[k] )


###### remaining columns to test ######
# female
# household-member
# income, pension
# income, cesantia
# income, dividend
# independiente
# literate
# student
# weight
# pension, contributing (if not pensioned)
# pension, receiving
# pension, contributor(s) (if not pensioned) = split
# pension, contributor(s) (if not pensioned) = self
# pension, contributor(s) (if not pensioned) = employer
# seguro de riesgos laborales (if reported)
# income, govt, cash
# income, govt, in-kind
# income, non-labor
# income, capital (tax def)
# income, private, cash
# income, private, in-kind
# income, donacion
# income, infrequent
# income, ganancia ocasional, 10%-taxable
# income, ganancia ocasional, 20%-taxable
# income, labor, cash
# income, labor, in-kind
# income, cash
# income, in-kind
# income
# income, govt
# income, private
# income, labor
# member-by-income
# race, indig
# race, git|rom
# race, raizal
# race, palenq
# race, neg|mul
# race, whi|mest
# disabled
# dependent
# income, borrowing


if True: # run tests
  # build data
  ppl = oio.readStage(cl.subsample, 'people_1')
  ppl["education"] = util.interpretCategorical( ppl["education"]
                                              , files.edu_key.values() )

  # integration test
  test_people( ppl )
