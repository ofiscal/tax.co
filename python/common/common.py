if True:
  from sys import argv
  import pandas as pd
  #
  import python.build.classes as cla
  if len( argv) > 1: # we are using the command line
    import python.common.params.command_line as imp
  else: # we are in the interpreter
    import python.common.params.repl         as imp

if True:
  subsample = imp.subsample
  strategy = imp.strategy
  regime_year = imp.regime_year
  strategy_suffix = imp.strategy_suffix
  strategy_year_suffix = imp.strategy_year_suffix

def retrieve_file( file_struct, subsample ):
  return pd.read_csv(
      ( "data/enph-2017/recip-" + str(subsample)
        + "/" + file_struct.filename )
      , usecols = list( cla.name_map( file_struct.col_specs )
                      . keys() )
    )

def collect_files( file_structs, subsample=subsample ):
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

