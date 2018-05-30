vat_pics_dir = "output/vat-pics/"


if True: # TODO: move this to build.py
  households["vat/income"] = households["vat-paid"] / households["income"]
  households["value/income"] = households["value"] / households["income"]
  people["vat/income"] = people["vat-paid"] / people["income"]
  people["value/income"] = people["value"] / people["income"]


if True: # stats about purchases
    plt.close()
    draw.single_cdf( purchases["quantity"], "CDF of quantity per purchase",
                     logx = True)
    draw.savefig( vat_pics_dir + "purchases" , "quantity" )

    plt.close()
    draw.single_cdf( purchases["frequency"], "CDF of purchase frequency",
                     logx = True)
    draw.savefig( vat_pics_dir + "purchases" , "frequency cdf" )

    plt.close()
    plt.title("Purchase frequency")
    plt.xticks( np.arange(1,11,1),
                ["Diario"
                 , "\"Varias veces\n por semana\""
                 , "Semanal"
                 , "Quincenal"
                 , "Mensual"
                 , "Bimestral"
                 , "Trimestral"
                 , "Anual"
                 , "\"Esporádico\""
                 , "Semestral"],
                rotation='vertical')
    plt.gcf().subplots_adjust(bottom=0.30) # labels go out of frame otherwise
    draw.table( purchases, "frequency-code" )
    draw.savefig( vat_pics_dir + "purchases" , "frequency" )

    plt.close()
    draw.single_cdf( purchases["value"], "CDF of monthly purchase value",
                     logx = True)
    draw.savefig( vat_pics_dir + "purchases" , "value" )

    plt.close()
    draw.single_cdf( purchases["vat-paid"], "CDF of VAT paid per purchase",
                     logx = True)
    draw.savefig( vat_pics_dir + "purchases" , "vat in pesos" )


if True: # stats about people
  if True: # single series
    plt.close()
    draw.single_cdf( people["age"], "CDF of age across individuals")
    draw.savefig( vat_pics_dir + "people" , "age" )

    plt.close()
    draw.single_cdf( people["education"], "CDF of education across individuals")
    draw.savefig( vat_pics_dir + "people" , "education" )

    plt.close()
    draw.single_cdf( people["value"], "CDF of spending per month across individuals",
                     logx = True)
    draw.savefig( vat_pics_dir + "people" , "spending per month" )

    plt.close()
    draw.single_cdf( people["value"], "CDF of income across individuals",
                     logx = True)
    draw.savefig( vat_pics_dir + "people" , "income" )

    plt.close()
    draw.single_cdf( people["transactions"], "CDF of transactions per month across individuals" )
    draw.savefig( vat_pics_dir + "people" , "transactions per month" )


if True: # stats about households with income
  if True: # build households_w_income from households
    # TODO ? move this data-building to an earlier-stage file

    households_w_income = households[ households["income"] > 0 ].copy()
      # Without the copy (even if I use .loc(), as suggested by the error)
      # this causes an error about modifying a view.
    households_w_income["one"] = 1
    households_w_income["income-decile"] = pd.qcut(
      households_w_income["income"], 10, labels = False, duplicates='drop')
    counts = households_w_income.groupby( "income-decile" )[["one"]]     \
           .agg('sum').rename(columns = {"one":"count"})
    mins = households_w_income.groupby( "income-decile" )[["income"]]    \
           .agg('min').rename(columns = {"income":"min"})
    maxs = households_w_income.groupby( "income-decile" )[["income"]]    \
           .agg('max').rename(columns = {"income":"max"})
    household_w_income_decile_summary = pd.concat([counts,mins,maxs],axis=1)

  if True: # CDF of spending / income
    plt.close()
    draw.single_cdf( households_w_income["value"] / households_w_income["income"],
                     "CDF of (spending / income) across households",
                     logx = True)
    draw.savefig( vat_pics_dir + "income households" , "spending over income" )

  if True: # the CDF of (VAT / income) by income decile
    plt.close()
    plt.title("The CDF of (VAT / income), by income decile")
    plt.xlabel("VAT paid / income")
    plt.ylabel("Probability")
    styles = [":","-",":","-",":","-",":","-",":","-"]
    colors = ["red","red","orange","orange","yellow","yellow",
              "green","green","purple","purple"]
    for i in list(household_w_income_decile_summary.index):
      draw.cdf( households_w_income                           \
                  [ households_w_income["income-decile"]==i ] \
                  [ "vat/income" ],
                linestyle = styles[i],
                color = colors[i],
                logx = True,
                xmin = 1/(10**6),
                with_mean = False
      )
    plt.grid(color='b', linestyle=':', linewidth=0.5)
    draw.savefig(vat_pics_dir + "income households", "VAT over income, by income decile.png")

  if True: # the CDF of (VAT / income) across households by has-child
    plt.close()
    plt.title("The CDF of (VAT / income) across households" + "\n" +
              "with (solid) and without (dashed) children")
    plt.xlabel("VAT paid / income")
    plt.ylabel("Probability")
    styles = ["-",":"]
    for (style,value) in [(0,False),(1,True)]:
      draw.cdf( households_w_income                      \
                  [ households_w_income["has-child"]==value ] \
                  [ "vat/income" ],
                linestyle = styles[style],
                with_mean = False,
                logx = True)
    plt.grid(color='b', linestyle=':', linewidth=0.5)
    draw.savefig(vat_pics_dir + "income households", "VAT over income, by has-child.png")

  if True: # the CDF of (VAT / income) across households by has-elderly
    plt.close()
    plt.title("The CDF of (VAT / income) across households" + "\n" +
              "without (solid) and with (dashed) an elderly member")
    plt.xlabel("VAT paid / income")
    plt.ylabel("Probability")
    styles = ["-",":"]
    for (style,value) in [(0,False),(1,True)]:
      draw.cdf( households_w_income                             \
                  [ households_w_income["has-elderly"]==value ] \
                  [ "vat/income" ],
                linestyle = styles[style],
                with_mean = False,
                logx = True)
    plt.grid(color='b', linestyle=':', linewidth=0.5)
    draw.savefig(vat_pics_dir + "income households", "VAT over income, by has-elderly.png")


if True: # stats about households
  if True: # single series
    plt.close()
    draw.single_cdf( households["members"], "Household size")
    draw.savefig(vat_pics_dir + "households" , "size")

    plt.close()
    draw.single_cdf( households["transactions"], "Transactions per month")
    draw.savefig( vat_pics_dir + "households" , "transactions per month" )

    plt.close()
    draw.single_cdf( households["age-min"], "Age of youngest member")
    draw.savefig( vat_pics_dir + "households" , "youngest" )

    plt.close()
    draw.single_cdf( households["age-max"], "Age of oldest member")
    draw.savefig( vat_pics_dir + "households" , "oldest" )

    plt.close()
    draw.single_cdf( households["income"], "Household income",
                     xmin = 10**4, # as a monthly income in pesos, that's basically zero
                     logx = True)
    draw.savefig( vat_pics_dir + "households" , "income" )

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
    plt.gcf().subplots_adjust(bottom=0.30) # labels go out of frame otherwise
    draw.table( households, "edu-max" )
    draw.savefig( vat_pics_dir + "households" , "max edu" )

  if True: # the CDF of (VAT / consumption) by income decile
    # PITFALL: Since 47% of households report zero income, nothing
      # distinguishes the first 5 deciles, so they are grouped together.
      # The "duplicates='drop'" option to pd.qcut achieves that grouping.

    draw.to_latex(
      util.tabulate_min_median_max_by_group( households, "income-decile", "income" ),
      "tex/tables/",
      "income by income decile"
    )

    draw.to_latex(
      util.tabulate_min_median_max_by_group( households, "income-decile", "vat/value" ),
      "tex/tables/",
      "vat over spending by income decile")

    plt.close()
    plt.title("The CDF of (VAT / consumption), by income decile")
    plt.xlabel("VAT paid / value consumed")
    plt.ylabel("Probability")
    styles = [":","-",":","-",":","-"]
    colors = ["red","red","green","green","blue","blue"]
    for i in list(household_decile_summary.index):
      draw.cdf( households                           \
                  [ households["income-decile"]==i ] \
                  ["vat/value"],
                linestyle = styles[i],
                color = colors[i],
                with_mean = False
      )
    plt.grid(color='b', linestyle=':', linewidth=0.5)
    draw.savefig(vat_pics_dir + "households", "VAT over consumption, by income decile.png")
