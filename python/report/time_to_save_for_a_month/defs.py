if True:
  from typing import List, Tuple
  import pandas as pd
  import numpy as np
  import weightedcalcs as weightLib


def months_to_save_for_a_month( income : float,
                                spending : float
                              ) -> float:
    return ( spending / (income - spending)
             if spending < income
             else 1e4 )

def mk_samples( df : pd.DataFrame
              ) -> List[ Tuple[ str, pd.DataFrame ] ]:
  return [ ("full sample",         df ),
           ("3 or more",           df[ df["members"] >= 3    ] ),
           ("female head",         df[ (df["female head"] > 0) ] ),
         # Surprisingly, this group's time to save hardly differs from "female head"
         # ("female head, plural", df[ (df["female head"] > 0) &
         #                             (df["members"] >= 2) ] ),
           ("has child",           df[ df["has-child"] > 0   ] ),
           ("all elderly",         df[ df["all-elderly"] > 0   ] ),
           ("some elderly",        df[ (df["has-elderly"] > 0) &
                                       (df["all-elderly"] < 1) ] )
          ]

def quantiles_report( samples : List[ Tuple[ str, pd.DataFrame ] ],
                      colname : str,
                      wc : weightLib.Calculator,
                      quantiles : List[float],
                      add_unity : bool = False,
                    ) -> pd.DataFrame:
    sample_names = list( map( lambda pair: pair[0],
                              samples ) )
    qd = pd.DataFrame( # quantile data
        columns = sample_names,
        index = quantiles + ( [1] if add_unity else [] ) )
    for q in quantiles:
        for (name,sample) in samples:
            qd[name][q] = wc.quantile( sample,
                                       colname,
                                       q )
    return ( qd.applymap(
               # PITFALL: This handles the case of NaN correctly
               # because NaN < x is false for all x.
               lambda x: x if x < 9999 else np.inf )
            . transpose() . round(2) )

