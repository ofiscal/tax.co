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

if True: # the CDF of (VAT / income) by income decile
  plt.close()
  plt.title("The CDF of (VAT / income), by income decile, for income-earning households")
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
              logx = True,
              xmin = 1/(10**6),
              with_mean = False
    )
  plt.grid(color='b', linestyle=':', linewidth=0.5)
  draw.savefig(vat_pics_dir + "income-households", "VAT-over-income,-by-income-decile.png")

if True: # the CDF of (VAT / income) across households by has-child
  plt.close()
  plt.title("The CDF of (VAT / income) across income-earning households" + "\n" +
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
  draw.savefig(vat_pics_dir + "income-households", "VAT-over-income,-by-has-child.png")

if True: # the CDF of (VAT / income) across households by has-elderly
  plt.close()
  plt.title("The CDF of (VAT / income) across income-earning households" + "\n" +
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
  draw.savefig(vat_pics_dir + "income-households", "VAT-over-income,-by-has-elderly.png")

if True: # the CDF of (VAT / income) across households by education
  plt.close()
  plt.title("The CDF of (VAT / income) across income-earning households"     + "\n" +
    "by maximum education level among a household's members." + "\n" +
    "(red = ninguno, orange = preescolar, yellow = primaria," + "\n" +
    "green = secundaria, blue = media, purple = superior,"    + "\n" +
    "black = no sabe")
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
              xmin = 0.00001, xmax = 0.5,
              logx = True)
  plt.grid(color='b', linestyle=':', linewidth=0.5)
  draw.savefig(vat_pics_dir + "income-households", "VAT-over-income,-by-max-edu.png")
