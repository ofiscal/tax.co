if True:
  from typing import List, Dict
  import pandas as pd


def unique( coll: List ) -> bool:
  return len( coll ) == len( set( coll ) )
