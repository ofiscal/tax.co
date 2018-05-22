if True: # the CDF of (VAT / consumption) by income decile
  # PITFALL: Because 47% of households report zero income, there is nothing
    # to distinguish the first five deciles, so they are grouped together.
    # The "duplicates='drop'" option to pd.qcut achieves that grouping.

  households["income-decile"] = pd.qcut(
    households["income"], 10, labels = False, duplicates='drop')
  households["one"] = 1
  counts = households.groupby( "income-decile" )[["one"]]     \
         .agg('sum').rename(columns = {"one":"count"})
  mins = households.groupby( "income-decile" )[["income"]]    \
         .agg('min').rename(columns = {"income":"min"})
  maxs = households.groupby( "income-decile" )[["income"]]    \
         .agg('max').rename(columns = {"income":"max"})
  decile_summary = pd.concat([counts,mins,maxs],axis=1)
  
  plt.title("The CDF of (VAT / consumption), by income decile")
  plt.xlabel("VAT paid / value consumed")
  plt.ylabel("Probability")
  styles = [":","-",":","-",":","-"]
  colors = ["red","red","green","green","blue","blue"]
  for i in list(decile_summary.index):
    draw.cdf( households[ households["income-decile"]==i ]    \
                        ["vat/value"],
              linestyle = styles[i],
              color = colors[i]
    )
  plt.savefig("vat over consumption by income decile.png")
