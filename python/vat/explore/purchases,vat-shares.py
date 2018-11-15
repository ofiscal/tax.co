import pandas as pd
import numpy as np

import python.build.output_io as oio

subsample = 10
purchases = oio.readStage( subsample, "purchases_2_vat" )

purchases["one"] = 1
total_obs = purchases["one"].sum()
total_value = purchases["value"].sum()

tbl_min = util.tabulate_stats_by_group( purchases, "vat, min", "value" )
tbl_min["share"] = tbl_min["count"] / total_obs
tbl_min["total_value"] = tbl_min["count"] * tbl_min["mean"]
tbl_min["value_share"] = tbl_min["total_value"] / total_obs
tbl_min

tbl_max = util.tabulate_stats_by_group( purchases, "vat, max", "value" )
tbl_max["share"] = tbl_max["count"] / total_obs
tbl_max["total_value"] = tbl_max["count"] * tbl_max["mean"]
tbl_max["value_share"] = tbl_max["total_value"] / total_obs
tbl_max
