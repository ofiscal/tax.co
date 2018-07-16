if True: # CDF of spending / income
  plt.close()
  draw.single_cdf( households_w_income["value"] / households_w_income["income"],
                   "CDF of (spending / income) across households",
                   xmin = 10**(-3), xmax = 10**3,
                   logx = True)
  draw.savefig( vat_pics_dir + "income-households" , "spending-over-income" )

if True: # the CDF of (VAT / income) by income decile
  plt.close()
  plt.title("The CDF of (VAT / income), by income decile")
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
  draw.savefig(vat_pics_dir + "income-households", "VAT-over-income,-by-has-child.png")

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
  draw.savefig(vat_pics_dir + "income-households", "VAT-over-income,-by-has-elderly.png")
