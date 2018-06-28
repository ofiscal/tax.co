if True: # single series
  plt.close()
  draw.single_cdf( people["age"], "CDF of age across individuals")
  draw.savefig( vat_pics_dir + "people" , "age" )

  plt.close()
  util.tabulate_series(people["education"]).plot.bar()
  draw.savefig( vat_pics_dir + "people" , "education" )

  plt.close()
  draw.single_cdf( people["value"], "CDF of spending per month across individuals",
                   logx = True)
  draw.savefig( vat_pics_dir + "people" , "spending-per-month" )

  plt.close()
  draw.single_cdf( people["value"], "CDF of income across individuals",
                   logx = True)
  draw.savefig( vat_pics_dir + "people" , "income" )

  plt.close()
  draw.single_cdf( people["transactions"], "CDF of transactions per month across individuals" )
  draw.savefig( vat_pics_dir + "people" , "transactions-per-month" )
