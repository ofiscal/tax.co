if True:
  from   datetime import datetime, timedelta
  import json
  import numpy as np
  import os
  import os.path as path
  import pandas as pd
  import subprocess
  from   typing import Callable, Dict
  #
  import python.common.common as c


tax_co_root_folder = "/mnt/tax.co"
users_folder     = os.path.join ( tax_co_root_folder,
                                  "users/" )
constraints_file = os.path.join ( tax_co_root_folder,
                                  "data/constraints-time-memory.json" )
requests_file    = os.path.join ( tax_co_root_folder,
                                  "data/requests.csv" )

with open ( constraints_file ) as f:
    constraints = json . load ( f )
