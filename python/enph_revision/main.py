# exec( open("python/enph_revision/main.py").read() )

import pandas as pd
import numpy as np
import os

exec( open("python/enph_revision/load_files.py").read() )
exec( open("python/enph_revision/clean.py").read() )
exec( open("python/enph_revision/coicop_search.py").read() )
