# The value-added tax.

import sys
import numpy as np
import pandas as pd
import python.util as util
import python.datafiles as datafiles
import python.vat.legends as vat_files
import python.vat.output_io as vat_output_io


subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.
files = list( vat_files.purchase_file_legends.keys() )


if True: # build the purchase data
  purchases = pd.DataFrame() # will accumulate from each file
  for file in files:
    legend = vat_files.purchase_file_legends[file]
    shuttle = pd.read_csv(
      datafiles.yearSubsampleSurveyFolder(2017,subsample) + file + '.csv'
      , usecols = list( legend.keys() )
    )
    shuttle = shuttle.rename(columns=legend) # homogenize column names across files
    shuttle["file-origin"] = file
  
    if False: # print summary stats for `shuttle`, before merging with `purchases`
      print( "\n\nFILE: " + file + "\n" )
      for colname in shuttle.columns.values:
        col = shuttle[colname]
        print("\ncolumn: " + colname)
        print("missing: " + str(len(col.index)-col.count())
              + " / "  + str(len(col.index)))
        print( col.describe() )

    purchases = purchases.append(shuttle)
  del(shuttle)
  vat_output_io.saveStage(subsample, purchases, '/1.purchases')


if True: # merge coicop, build money-valued variables
  coicop_vat = pd.read_csv( "data/vat/coicop-vat.csv", sep=';' )
  purchases = purchases.merge( coicop_vat, on="coicop" )

  purchases["price"] = purchases["value"] / purchases["quantity"]
  purchases["per-purchase value"] = purchases["value"]
  purchases["frequency-code"] = purchases["frequency"]
    # kept for the sake of drawing a table of purchase frequency
    # with frequencies spread evenly across the x-axis
  purchases["frequency"].replace( vat_files.frequency_legend, inplace=True )
  purchases["value"] = purchases["frequency"] * purchases["value"]
  purchases["vat-paid"] = purchases["value"] * purchases["vat-rate"]

  vat_output_io.saveStage(subsample, purchases, '/2.purchases,prices,taxes')
