# Some simple definitions needed throughout much of the codebase.

if True:
  from os import path
  import sys
  from sys import argv
  import json
  import pandas as pd
  import hashlib
  #
  import python.build.classes as cla
  import python.common.terms as terms


if len( argv) > 1: # If we are using the command line.
  config_file = sys.argv[1]
else:              # If we are in the interpreter.
  config_file = "config/repl.json"

if True: # For validation, mostly.
         # (`valid_subsamples` is also looped over, in another program.)
  valid_strategies = [ # There used to be a lot of these.
    terms.detail ]     # They disappeared in branch "retire-hypotheticals".
  valid_subsamples = [1,10,100,1000]
  valid_regime_years = [2016, 2018, 2019]

with open( config_file ) as f:
  config_dict = json.load( f )

subsample = int( config_dict["subsample"] )
if not subsample in valid_subsamples:
  raise ValueError( "invalid subsample reciprocal: " + str(subsample) )

strategy = config_dict["strategy"]
if not strategy in valid_strategies:
  raise ValueError( "invalid strategy: " + strategy )

regime_year = config_dict["regime_year"]
if not regime_year in valid_regime_years:
  raise ValueError( "invalid tax regime year: " + str(regime_year) )

vat_by_coicop = config_dict["vat_by_coicop"]
if not path.exists( vat_by_coicop ):
  raise ValueError( "File does not exist: " + vat_by_coicop )

vat_by_capitulo_c = config_dict["vat_by_capitulo_c"]
if not path.exists( vat_by_capitulo_c ):
  raise ValueError( "File does not exist: " + vat_by_capitulo_c )

user_email = config_dict [ "user_email" ]
user = ( # A user's "name" is generated from their email address.
    hashlib.md5(
        user_email . encode () )
    . hexdigest () )

strategy_suffix = strategy
strategy_year_suffix = strategy + "." + str(regime_year)

def retrieve_file( file_struct, subsample ):
  return pd.read_csv(
      ( "data/enph-2017/recip-" + str(subsample)
        + "/" + file_struct.filename )
      , usecols = list( cla.name_map( file_struct.col_specs )
                      . keys() )
    )

def collect_files( file_structs, subsample=subsample ):
  """Collect all files in `file_structs` into a single dataset,
with slight changes for homogeneity, readability."""
  acc = pd.DataFrame()
  for f in file_structs:
    shuttle = ( retrieve_file( f, subsample )
              . rename( columns = cla.name_map( f.col_specs ) ) )
    # shuttle["file-origin"] = f.name
    for c in f.corrections:
      shuttle = c.correct( shuttle )
    acc = acc.append( shuttle
                    , ignore_index = True # avoids duplicating index values
                    , sort=True ) # the two capitulo_c files include a column,
    # "25-broad-categs", that the others don't. `sort=true` deals with that.
  return acc
