if True: # single series
  plt.close()
  draw.single_cdf( people["age"], "CDF of age across individuals")
  draw.savefig( vat_pics_dir + "people" , "age" )

  plt.close()
  util.tabulate_series(people["education"]).plot.bar()
  draw.savefig( vat_pics_dir + "people" , "education" )

  if True: # income, logx and normal
    plt.close()
    draw.single_cdf( people["income"], "CDF of income across individuals",
                     xmin = 10**5, xmax = 4e6 )
    draw.savefig( vat_pics_dir + "people" , "income" )

    plt.close()
    draw.single_cdf( people["income"], "CDF of income across individuals",
                     xmin = 10**5, xmax = 10**7, logx = True)
    draw.savefig( vat_pics_dir + "people/logx" , "income" )
  
  plt.close()
  draw.single_cdf( people["value"],
                   "CDF of spending per month across individuals",
                   logx = True)
  draw.savefig( vat_pics_dir + "people" , "spending-per-month" )

  plt.close()
  draw.single_cdf( people["transactions"],
                   "CDF of transactions per month across individuals" )
  draw.savefig( vat_pics_dir + "people" , "transactions-per-month" )


if True: # age deciles
  # TODO ? unify this with util.tabulate_min_median_max_by_group
  ageGroups = people[["age-decile","age"]].groupby("age-decile")
  ageMins = ageGroups.agg("min").rename(columns={"age":"min"})
  ageMaxs = ageGroups.agg("max").rename(columns={"age":"max"})
  ageDeciles = pd.concat([ageMins,ageMaxs],axis=1)
  draw.to_latex( ageDeciles,
                 "output/vat-tables/recip-" + str(subsample),
                 "age-by-age-decile" )

if True: # the CDF of income across individuals by age decile
  plt.close()
  plt.title("The CDF of income across"     + "\n" +
    "individuals by age decile." + "\n" +
    "(The youngest are solid lines, the oldest are dashed." + "\n" +
    "Within those two groups, the youngest are red, the oldest blue.)" )
  plt.xlabel("Income")
  plt.ylabel("Probability")
  styles = ["-"  ,"-"     ,"-"     ,"-"     ,"-",
            ":"  ,":"     ,":"     ,":"     ,":"]
  colors = ["red","orange","yellow", "green","blue",
            "red","orange","yellow", "green","blue"]
  for styleIndex in list(range(1,10)):
    draw.cdf( people                            \
                [ people["age-decile"]==float(styleIndex) ] \
                [ "income" ],
              linestyle = styles[styleIndex],
              color = colors[styleIndex],
              with_mean = False,
              xmin = 10**5, xmax = 10**7,
              logx = True)
  plt.grid(color='b', linestyle=':', linewidth=0.5)
  draw.savefig(vat_pics_dir + "people", "income,by-age-decile.png")
