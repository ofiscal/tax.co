from typing import List
import re as regex


def rename_monthly( cols: List[str] ):
  return [ regex.sub( "year", "month", col )
           for col in cols ]
