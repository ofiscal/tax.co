# This used to merge the purchase data into the person-level data,
# and compute some new variables.
# Now it only does the latter.
# TODO : absorb this code into an adjacent program.

if True:
  import sys
  import pandas as pd
  #
  import python.common.util as util
  import python.build.output_io as oio
  import python.common.common as c


if True: # input files
  people = oio.readStage( c.subsample, "people_2_buildings" )

if True: # these don't use the purchase data; they could be elsewhere
    people["age-decile"] = pd.qcut(
      people["age"], 10, labels = False, duplicates='drop')
    people["income-decile"] = (
      # PITFALL: there's a different such variable at the household level
      util.noisyQuantile( 10, 0, 1, people["income"] ) )
    people["female head"] = people["female"] * (people["household-member"]==1)


oio.saveStage( c.subsample, people,
               'people_3_purchases.' + c.strategy_suffix )
