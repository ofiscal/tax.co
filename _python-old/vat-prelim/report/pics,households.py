if True: # stats about households
  if True: # single series
    plt.close()
    draw.single_cdf( households["members"], "Household size", xmax = 10)
    draw.savefig(vat_pics_dir + "households" , "size")

    plt.close()
    draw.single_cdf( households["transactions"], "Transactions per month", xmax = 150)
    draw.savefig( vat_pics_dir + "households" , "transactions-per-month" )

    plt.close()
    draw.single_cdf( households["age-min"], "Age of youngest member")
    draw.savefig( vat_pics_dir + "households" , "youngest" )

    plt.close()
    draw.single_cdf( households["age-max"], "Age of oldest member")
    draw.savefig( vat_pics_dir + "households" , "oldest" )

    if True: # household income, logx and linear x
      plt.close()
      draw.single_cdf( households["income"], "Household income",
                       xmax = 3e6)
      plt.gca().xaxis.set_major_formatter(EngFormatter(places=2))
      draw.savefig( vat_pics_dir + "households" , "income" )

      plt.close()
      draw.single_cdf( households["income"], "Household income",
                       xmin = 10**4, # as a monthly income in pesos, that's basically zero
                       logx = True)
      draw.savefig( vat_pics_dir + "households/logx" , "income" )
  
    plt.close()
    plt.title("Highest education level among household members")
    plt.xticks( np.arange(1,10,1),
                [ "Ninguno",
                  "Preescolar",
                  "Basica\n Primaria",
                  "Basica\n Secundaria",
                  "Media",
                  "Superior o\n Universitaria",
                  "(unused\n value)",
                  "(unused\n value)",
                  "No sabe,\n no informa" ],
                rotation='vertical')
    draw.table( households, "edu-max" )
    draw.savefig( vat_pics_dir + "households" , "max-edu" )

  if True: # VAT expenditures by income decile
    # PITFALL: Since 47% of households report zero income, nothing
      # distinguishes the first 5 deciles, so they are grouped together.
      # The "duplicates='drop'" option to pd.qcut achieves that grouping.

    draw.to_latex(
      util.tabulate_min_median_max_by_group( households, "income-decile", "income" ),
      "output/vat-tables/recip-" + str(subsample),
      "income-by-income-decile"
    )

    draw.to_latex(
      util.tabulate_min_median_max_by_group( households, "income-decile", "vat/value" ),
      "output/vat-tables/recip-" + str(subsample),
      "vat-over-spending-by-income-decile")

    if True: # two CDFs on a figure
      plt.close()

      plt.suptitle("CDFs of VAT expenditure across households by income decile")

      plt.subplot(1,2,1)
      plt.xlabel("VAT paid / value consumed")
      plt.ylabel("Probability")
      styles = [":","-",":","-",":","-"]
      colors = ["red","red","green","green","blue","blue"]
      for i in list(households_decile_summary.index):
        draw.cdf( households                           \
                    [ households["income-decile"]==i ] \
                    ["vat/income"],
                  linestyle = styles[i],
                  color = colors[i],
                  xmax = 0.1,
                  with_mean = False
        )
      plt.grid(color='b', linestyle=':', linewidth=0.5)

      plt.subplot(1,2,2)
      plt.ylabel("Probability")
      styles = [":","-",":","-",":","-"]
      colors = ["red","red","green","green","blue","blue"]
      for i in list(households_decile_summary.index):
        draw.cdf( households                           \
                    [ households["income-decile"]==i ] \
                    ["vat/value"],
                  linestyle = styles[i],
                  color = colors[i],
                  xmax = 0.1,
                  with_mean = False
        )
      plt.grid(color='b', linestyle=':', linewidth=0.5)

      ax = plt.gca()
      ax.set_yticklabels([])
    
      fig = plt.gcf()
      fig.set_size_inches(8,4)

      draw.savefig(vat_pics_dir + "households", "VAT-over-consumption,-by-income-decile.png")
