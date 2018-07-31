# TODO: Centralize this code, which is (nearly) duplicated between build_late.py and main,people.py
edu_key = { 1 : "Ninguno",
      2 : "Preescolar",
      3 : "Basica\n Primaria",
      4 : "Basica\n Secundaria",
      5 : "Media",
      6 : "Superior o\n Universitaria",
      9 : "No sabe,\n no informa" }
households_w_income["edu-max"] = pd.Series( pd.Categorical(
    pd.Categorical( households_w_income["edu-max"]
                   , categories = list( edu_key.values() )
                   , ordered = True) ) )

if True: # CDF of spending / income
  plt.close()
  draw.single_cdf( households_w_income["value"] / households_w_income["income"],
                   "CDF of (spending / income) across income-earning households",
                   xmin = 10**(-3), xmax = 10**3,
                   logx = True)
  draw.savefig( vat_pics_dir + "income-households" , "spending-over-income" )

if True: # CDFs of VAT by income decile
  plt.close()

  plt.suptitle("CDFs of VAT, by income decile, for income-earning households." + "\n"
            + "(dashed red = least income decile, solid purple = greatest)" )

  plt.subplot(1,2,1)
  plt.xlabel("VAT paid / income")
  plt.ylabel("Probability")
  styles = [":","-",":","-",":","-",":","-",":","-"]
  colors = ["red","red","orange","orange","yellow","yellow",
            "green","green","purple","purple"]
  for i in list(households_w_income_decile_summary.index):
    draw.cdf( households_w_income                           \
                [ households_w_income["income-decile"]==i ] \
                [ "vat/income" ],
              linestyle = styles[i],
              color = colors[i],
              xmax = 0.15,
              with_mean = False
    )
  plt.grid(color='b', linestyle=':', linewidth=0.5)

  plt.subplot(1,2,2)
  plt.xlabel("VAT paid / spending")
  styles = [":","-",":","-",":","-",":","-",":","-"]
  colors = ["red","red","orange","orange","yellow","yellow",
            "green","green","purple","purple"]
  for i in list(households_w_income_decile_summary.index):
    draw.cdf( households_w_income                           \
                [ households_w_income["income-decile"]==i ] \
                [ "vat/value" ],
              linestyle = styles[i],
              color = colors[i],
              xmax = 0.15,
              with_mean = False
    )
  plt.grid(color='b', linestyle=':', linewidth=0.5)

  ax = plt.gca()
  ax.set_yticklabels([])

  fig = plt.gcf()
  fig.set_size_inches(8,4)

  draw.savefig(vat_pics_dir + "income-households", "VAT-over-income,-by-income-decile.png")

if True: # CDFs of VAT across households by has-child
  plt.close()
  plt.suptitle("Two CDFs of VAT across income-earning households" + "\n" +
               "with (solid) and without (dashed) children")

  plt.subplot(1,2,1)
  plt.xlabel("VAT paid / income")
  plt.ylabel("Probability")
  styles = ["-",":"]
  for (style,value) in [(0,False),(1,True)]:
    draw.cdf( households_w_income                      \
                [ households_w_income["has-child"]==value ] \
                [ "vat/income" ],
              linestyle = styles[style],
              xmax = 0.1,
              with_mean = False )
  plt.grid(color='b', linestyle=':', linewidth=0.5)

  plt.subplot(1,2,2)
  plt.xlabel("VAT paid / spending")
  styles = ["-",":"]
  for (style,value) in [(0,False),(1,True)]:
    draw.cdf( households_w_income                      \
                [ households_w_income["has-child"]==value ] \
                [ "vat/value" ],
              linestyle = styles[style],
              xmax = 0.1,
              with_mean = False )
  plt.grid(color='b', linestyle=':', linewidth=0.5)

  ax = plt.gca()
  ax.set_yticklabels([])

  fig = plt.gcf()
  fig.set_size_inches(8,4)

  draw.savefig(vat_pics_dir + "income-households", "VAT-over-income,-by-has-child.png")

if True: # the CDF of (VAT / income) across households by has-elderly
  plt.close()
  plt.suptitle("CDFs of VAT across income-earning households" + "\n" +
            "without (solid) and with (dashed) an elderly member")

  plt.subplot(1,2,1)
  plt.xlabel("VAT paid / income")
  plt.ylabel("Probability")
  styles = ["-",":"]
  for (style,value) in [(0,False),(1,True)]:
    draw.cdf( households_w_income                             \
                [ households_w_income["has-elderly"]==value ] \
                [ "vat/income" ],
              linestyle = styles[style],
              xmax = 0.1,
              with_mean = False )
  plt.grid(color='b', linestyle=':', linewidth=0.5)

  plt.subplot(1,2,2)
  plt.xlabel("VAT paid / income")
  styles = ["-",":"]
  for (style,value) in [(0,False),(1,True)]:
    draw.cdf( households_w_income                             \
                [ households_w_income["has-elderly"]==value ] \
                [ "vat/value" ],
              linestyle = styles[style],
              xmax = 0.1,
              with_mean = False )
  plt.grid(color='b', linestyle=':', linewidth=0.5)

  ax = plt.gca()
  ax.set_yticklabels([])

  fig = plt.gcf()
  fig.set_size_inches(8,4)

  draw.savefig(vat_pics_dir + "income-households", "VAT-over-income,-by-has-elderly.png")

if True: # the CDF of (VAT / income) across households by education
  plt.close()

  plt.suptitle("CDFs of VAT across income-earning households, by max education level among its members.\n" +
    "(red = ninguno, orange = preescolar, yellow = primaria, green = secundaria,\n" +
    "blue = media, purple = superior, black = no sabe")

  plt.subplot(1,2,1)
  plt.xlabel("VAT paid / income")
  plt.ylabel("Probability")
  colors = ["red","orange","yellow", "green","blue","purple","black"]
  categs = list(households_w_income["edu-max"].cat.categories)
  for (color,categ) in zip ( list (range (0, len(categs))), categs):
    draw.cdf( households_w_income                             \
                [ households_w_income["edu-max"]==categ ] \
                [ "vat/income" ],
              color = colors[color],
              with_mean = False,
              xmax = 0.1 )
  plt.grid(color='b', linestyle=':', linewidth=0.5)

  plt.subplot(1,2,2)
  plt.xlabel("VAT paid / income")
  colors = ["red","orange","yellow", "green","blue","purple","black"]
  categs = list(households_w_income["edu-max"].cat.categories)
  for (color,categ) in zip ( list (range (0, len(categs))), categs):
    draw.cdf( households_w_income                             \
                [ households_w_income["edu-max"]==categ ] \
                [ "vat/value" ],
              color = colors[color],
              with_mean = False,
              xmax = 0.1 )
  plt.grid(color='b', linestyle=':', linewidth=0.5)

  ax = plt.gca()
  ax.set_yticklabels([])

  fig = plt.gcf()
  fig.set_size_inches(8,4)

  draw.savefig(vat_pics_dir + "income-households", "VAT-over-income,-by-max-edu.png")
