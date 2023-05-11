# PITFALL: Naming this module `subprocess` generates conflicts,
# causing Python to fail to find the built-in `subprocess` library.

if True:
  import os
  import subprocess
  from   typing import List
  #
  import python.common.common as c

def run ( to_run : List[ str ] # A list of lexemes -- that is,
          # would be space-separated tokens at the command line.
        , log_path : str
        , stdout_path : str
        , stderr_path : str
        ):

  if True: # Refine the environment.
    my_env = os . environ . copy ()
    env_additions = ":" . join (
      [ c.tax_co_root] )
    my_env["PYTHONPATH"] = (
      ":" . join ( [ env_additions,
                     my_env [ "PYTHONPATH" ] ] )
      if "PYTHONPATH" in my_env . keys ()
      else env_additions )

  with open( log_path, "a" ) as f:
    f . write(
      "\n".join( [ "About to run this:" ] + to_run
                 + [ "", "in this environment: "
                   , str( my_env )
                   , "" ] ) )

  sp = subprocess.run (
    to_run,
    cwd    = c.tax_co_root,
    env    = my_env,
    stdout = subprocess . PIPE,
    stderr = subprocess . PIPE )

  for ( path, source ) in [ (stdout_path, sp.stdout),
                            (stderr_path, sp.stderr) ]:
    with open ( path, "a" ) as f:
      f . write ( source . decode () )

  return sp
