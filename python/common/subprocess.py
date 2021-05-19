import os
import subprocess
from   typing import List


tax_co_root_path = "/mnt/tax_co"

def run ( to_run : List[ str ] # A list of lexemes -- that is,
          # would be space-separated tokens at the command line.
        , log_path : str
        , stdout_path : str
        , stderr_path : str
        ):

  if True: # Refine the environment.
    my_env = os . environ . copy ()
    env_additions = ":" . join (
      [ tax_co_root_path,
        "/opt/conda/lib/python3.8/site-packages" ] )
      # TODO ? Why must this second folder be specified?
      # It's the default when I run python3 from the shell.
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
    cwd    = tax_co_root_path,
    env    = my_env,
    stdout = subprocess . PIPE,
    stderr = subprocess . PIPE )

  for ( path, source ) in [ (stdout_path, sp.stdout),
                            (stderr_path, sp.stderr) ]:
    with open ( os.path.join ( user_root, path ),
                "a" ) as f:
      f . write ( source . decode () )

  return sp
