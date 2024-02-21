# PITFALL: Calling this module "types" can, unbelievably,
# create mayhem due to collisions with
# the names of builtin modules.

from typing import Callable, List, Tuple
from typing_extensions import TypeAlias


AverageTaxBracket : TypeAlias = (
  Tuple [ float,       # minimum income threshold
            Callable [ # computes taxable base from wage
              [float], float ],
            float ] )  # average (not marginal!) tax rate

AverageTaxSchedule : TypeAlias = (
  List [ AverageTaxBracket ] )
