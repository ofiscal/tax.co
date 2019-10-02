from typing import List, Set
import numpy as np
import re as regex


def rename_monthly( cols: List[str] ):
  return [ regex.sub( "year", "month", col )
           for col in cols ]


### counting things in a space-separated list of integers

def count_num_matches_in_space_separated_list(
      list_as_str : str # a space-separated list of integers
    , targets : Set[int]  ):
  """ Counts how many times anything from the list argument appears in the string. """
  stripped = list_as_str . strip()
  if stripped in [np.nan, ""]: return 0
  else:
    num_list = map( float
                  , stripped . split(" ") )
    sources = filter( lambda x: x in targets, num_list )
    return len( list( sources ) )

public_codes = {2,3,4}
private_codes = set( range(1,11) ) - public_codes

def count_public( list_as_str : str ):
  """ Count public sources of funding in the "non-beca sources" variable. """
  return count_num_matches_in_space_separated_list(
    list_as_str, public_codes )

def count_private( list_as_str : str ):
  """ Count private sources of funding in the "non-beca sources" variable. """
  return count_num_matches_in_space_separated_list(
    list_as_str, private_codes )
