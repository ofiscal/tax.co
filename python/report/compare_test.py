"""
The only way to test this is manually,
by drawing a comparison of some simple data,
looking at the picture, and verifying it makes sense.
"""

import pandas as pd
import python.report.compare as comp


small = pd.DataFrame (
  data = { "measure" : ["x"],
           income_deciles[ 0] : [ 0],
           income_deciles[ 1] : [ 1],
           income_deciles[ 2] : [ 2],
           income_deciles[ 3] : [ 3],
           income_deciles[ 4] : [ 4],
           income_deciles[ 5] : [ 5],
           income_deciles[ 6] : [ 6],
           income_deciles[ 7] : [ 7],
           income_deciles[ 8] : [ 8],
           income_deciles[ 9] : [ 9] },
  columns = ["measure"] + income_deciles )

big = pd.DataFrame (
  data = { "measure" : ["x"],
           income_deciles[ 0] : [10],
           income_deciles[ 1] : [11],
           income_deciles[ 2] : [12],
           income_deciles[ 3] : [13],
           income_deciles[ 4] : [14],
           income_deciles[ 5] : [15],
           income_deciles[ 6] : [16],
           income_deciles[ 7] : [17],
           income_deciles[ 8] : [18],
           income_deciles[ 9] : [19] },
  columns = ["measure"] + income_deciles )

comp.draw_one_comparison (
  measure = "x",
  unit = "x",
  user = small,
  baseline = big,
  save_path = "test-compare" )
