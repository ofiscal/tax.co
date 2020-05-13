if True:
  import pandas as pd
  import numpy as np
  from typing import List, Tuple
  #
  import python.build.classes as cl
  import python.common.common as cm
  import python.build.output_io as oio
  from python.common.util import describeWithMissing, noisyQuantile
  import matplotlib
  import matplotlib.pyplot as plt
  import weightedcalcs as weightLib


wc = weightLib.Calculator('weight')

hh = oio.readStage(
    cm.subsample
  , "households_2_purchases." + cm.strategy_year_suffix )

hh = hh[ ~ ( hh["income"].isnull()
           | hh["value"].isnull() ) ]

def months_to_save_for_a_month( income : float,
                                spending : float
                              ) -> float:
    return ( spending / (income - spending)
             if spending <= income
             else 1e4 )

hh["months to save for a month"] = hh.apply(
    lambda row: months_to_save_for_a_month(
        income = row["income"],
        spending = row["value"] ),
    axis = "columns" )

hh["months to save for a month, cash"] = hh.apply(
    lambda row: months_to_save_for_a_month(
        income = row["income, cash"],
        spending = row["value"] ),
    axis = "columns" )

if False: # explore
  hh["months to save for a month"].describe()
  hh["used savings"].describe()
  hh["recently bought this house"].describe()
  #
  len(hh)
  len( hh[ hh["used savings"] > 0 ] )
  len( hh[ hh["recently bought this house"] > 0 ] )

hh = hh[ hh["used savings"] <= 0 ]
hh = hh.drop( columns = ["used savings"] )

def mk_samples( df : pd.DataFrame
              ) -> List[ Tuple[ str, pd.DataFrame ] ]:
  return [ ("full sample", df ),
           ("3 or more",   df[ df["members"] >= 3    ] ),
           ("female head", df[ df["female head"] > 0 ] ),
           ("has child",   df[ df["has-child"] > 0   ] ),
           ("has elderly", df[ df["has-elderly"] > 0 ] ) ]

def quantiles_report( samples : List[ Tuple[ str, pd.DataFrame ] ],
                      colname : str,
                      quantiles : List[float],
                      add_unity : bool = False
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

deciles = list( np.round(
    np.arange( 0, 1, 0.1 ),
    1 ) )

zoom_quantiles = list( np.round(
    np.arange( 0.32, 0.45001, 0.01 ),
    2 ) )

every = quantiles_report(
    mk_samples(
        # full sample gives just about identical results
        hh[ hh["recently bought this house"] <= 0 ] ),
    "months to save for a month, cash",
    deciles,
    add_unity = True )

zoom = quantiles_report(
    mk_samples(
        # full sample gives just about identical results
        hh[ hh["recently bought this house"] <= 0 ] ),
    "months to save for a month, cash",
    zoom_quantiles )


every_ = quantiles_report(
    mk_samples(
        # full sample gives just about identical results
        hh[ hh["recently bought this house"] <= 0 ] ),
    "months to save for a month",
    deciles,
    add_unity = True )

zoom_ = quantiles_report(
    mk_samples(
        # full sample gives just about identical results
        hh[ hh["recently bought this house"] <= 0 ] ),
    "months to save for a month",
    zoom_quantiles )


############## EXPERIMENTAL ##############

# hh["to plot"] = noisyQuantile(
#     10, 0, 0.01,
#     hh["months to save for a month"] )

# Inactive: plots
# fig, ax = plt.subplots()
# ax = hh['to plot'].value_counts().plot(
#     kind='bar',
#     figsize=(14,8),
#     title="title")
# ax.set_xlabel("xlabel")
# ax.set_ylabel("ylabel")
# 
# plt.savefig("temp.png")

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


plt.close()
labels = ['G1', 'G2', 'G3', 'G4', 'G5']
men_means = [20, 34, 30, 35, 27]
women_means = [25, 32, 34, 20, 25]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, men_means, width, label='Men')
rects2 = ax.bar(x + width/2, women_means, width, label='Women')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.savefig("temp.png")
