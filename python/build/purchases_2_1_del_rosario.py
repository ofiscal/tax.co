# REQUIREMENT: The list of goods to exempt should be in decreasing order of total expenditure
# (among the bottom 6 deciles of household income). This is automatic in the case of
# del_rosario_exemption_source = "auto".

# PITFALL: In this file, the 3rd command-line argument means something different,
# and there is a fourth. They are still parsed by the `common` library.

import pandas as pd
import numpy as np

import python.build.output_io as oio
import python.build.common as common


#class common:
#  subsample = 100
#  vat_strategy = "del_rosario"
#  del_rosario_exemption_source = "auto"
#  del_rosario_exemption_count = 10


## ## ## ## ## Read, prepare individual data sets ## ## ## ##
if      common.del_rosario_exemption_source == 'auto':
  exemptions = pd.read_csv( "output/vat/tables/recip-" + str(common.subsample)
                            + "/goods,first_six_deciles.csv"
                          , usecols = ["coicop"]
                          , dtype = {"coicop" : "str"}
                          )
elif common.del_rosario_exemption_source == 'manual':
  exemptions = pd.read_csv( "data/vat/exemptions"
                            + "/goods,first_six_deciles.csv"
                          , usecols = ["coicop"]
                          , dtype = {"coicop" : "str"}
                          )

exemptions = exemptions.head( common.del_rosario_exemption_count )
exemptions["exempt"] = 1


ps = pd.read_csv( "output/vat/data/recip-" + str(common.subsample) + "/purchases_2_vat.detail_.csv"
                  , dtype = {"coicop" : "str"}
)


## ## ## ## ## Construct the counterfactual ## ## ## ##
ps = ps.merge( exemptions, on = "coicop", how="left" )

vat_columns = ps.filter(regex="vat").columns
ps.loc[ ps["exempt"]==1, vat_columns ] = 0 # implement the counterfactual

ps = ps.drop( columns = "exempt" )


## ## ## ## ## Save ## ## ## ##
oio.saveStage( common.subsample
             , ps
             , "purchases_2_1_del_rosario." + common.vat_strategy_suffix )


## ## ## ## ## A way to test ## ## ## ##
# Before the line marked "implement the counterfactual" above,
# define these:
#     before0 = util.describeWithMissing( ps[ ~ (ps["exempt"]==1) ] )
#     before1 = util.describeWithMissing( ps[   (ps["exempt"]==1) ] )
# After it, define these:
#     after0 = util.describeWithMissing( ps[ ~ (ps["exempt"]==1) ] )
#     after1 = util.describeWithMissing( ps[   (ps["exempt"]==1) ] )
# before0 - after0 should be zero.
# before1[vat_columns] - after1[vat_columns] should be positive.
# The rest of the difference between before1 and after1 should also be 0.
