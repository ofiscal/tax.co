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

#if True:
hh = oio.readStage(
    cm.subsample
  , "households." + cm.strategy_year_suffix )

def months_to_save_for_a_month(
    income : float, spending : float ) -> float:
  if spending >= income:
      return 1e4
  else: return spending / (income - spending)

hh["months to save for a month"] = hh.apply(
    lambda row: months_to_save_for_a_month(
        row["income"],
        row["value"] ),
    axis = "columns" )

hh["months to save for a month, cash"] = hh.apply(
    lambda row: months_to_save_for_a_month(
        row["income, cash"],
        row["value"] ),
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
           ("3 or more", df[ df["members"] >= 3] ),
           ("female head", df[ df["female head"] > 0 ] ),
           ("has child", df[ df["has-child"] > 0 ] ),
           ("has elderly", df[ df["has-elderly"] > 0 ] ) ]

def quantiles_report( samples : List[ Tuple[ str, pd.DataFrame ] ],
                      quantiles : List[float]
                    ) -> pd.DataFrame:
    sample_names = list( map( lambda pair: pair[0],
                              samples ) )
    qd = pd.DataFrame( # quantile data
        columns = sample_names,
        index = quantiles + [1] )
    for q in quantiles:
        for (name,sample) in samples:
            qd[name][q] = wc.quantile(
                sample,
                "months to save for a month",
                q )
    return ( qd.applymap(
               # PITFALL: This handles the case of NaN correctly
               # because NaN < x is false for all x.
               lambda x: x if x < 9999 else np.inf )
            . transpose() . round(2) )

deciles = [ 0.1, 0.2, 0.3, 0.4, # quantiles (deciles)
           0.5, 0.6, 0.7, 0.8, 0.9]

decile_6 = [ 0.57, 0.58, 0.59,
             0.60, 0.61, 0.62, 0.63 ]

( quantiles_report(
    mk_samples(
        # full sample gives just about identical results
        hh[ hh["recently bought this house"] <= 0 ] ),
    deciles ) )

( quantiles_report(
    mk_samples(
        # full sample gives just about identical results
        hh[ hh["recently bought this house"] <= 0 ] ),
    decile_6 ) )


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
