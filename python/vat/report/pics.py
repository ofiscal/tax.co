vat_pics_dir = "output/vat-pics/"

if True: # summary stats about households
  plt.close()
  draw.single_cdf( households["members"], "Household Size",
                   vat_pics_dir + "households/" + "size")

  plt.close()
  draw.single_cdf( households["transactions"], "Transactions per month",
                   vat_pics_dir + "households/" + "transactions per month")

  plt.close()
  draw.single_cdf( households["age-min"], "Age of youngest member",
                   vat_pics_dir + "households/" + "youngest")

  plt.close()
  draw.single_cdf( households["age-max"], "Age of oldest member",
                   vat_pics_dir + "households/" + "oldest")

  plt.close()
  draw.single_cdf( households["income"], "Household income",
                   vat_pics_dir + "households/" + "income",
                   logx = True)

  plt.close()
  plt.xticks( np.arange(1,10,1),
              [ "Ninguno",
                "Preescolar",
                "Basica Primaria",
                "Basica Secundaria",
                "Media",
                "Superior o Universitaria",
                "(unused value)",
                "(unused value)",
                "No sabe, no informa" ],
              rotation='vertical')
  draw.single_cdf( households["edu-max"], "Highest education level among household members",
                   vat_pics_dir + "households/" + "max edu")

if True: # the CDF of (VAT / consumption) by income decile
  # PITFALL: Because 47% of households report zero income, there is nothing
    # to distinguish the first five deciles, so they are grouped together.
    # The "duplicates='drop'" option to pd.qcut achieves that grouping.

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
  plt.savefig(vat_pics_dir + "VAT over consumption by income decile.png")
