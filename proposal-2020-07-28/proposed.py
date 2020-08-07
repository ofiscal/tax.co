# PITFALL: All values are in UVT.

# Dividend tax rates

def dividendTax (x):
  return        ( 0                    if x < 300
    else        ( (x - 300 )*0.1       if x < 600
      else      ( (x - 600 )*0.12 + 30 if x < 1000
        else    ( (x - 1000)*0.18 + 78 if x < 1500
          else  ( (x - 1500)*0.2  + 168 ) ) ) ) )


# * Income tax rates

# Main> go incomeFormula1 incomeBrackets
# 0                         if x < (1090)
# (x - 1090  )*0.19         if x < (1700)
# (x - 1700  )*0.28 + 116   if x < (4100)
# (x - 4100  )*0.33 + 788   if x < (8670)
# (x - 8670  )*0.35 + 2296  if x < (18970)
# (x - 18970 )*0.39 + 5901  if x < (27595)
# (x - 27595 )*0.44 + 9265  if x < (36000)
# (x - 36000 )*0.47 + 12963 if x < (55000)
# (x - 55000 )*0.5  + 21893 if x < (90000)
# (x - 90000 )*0.55 + 39393 otherwise

# The table in the proposal differs slightly from this:
# written like the above pseudo-Python, its last row would look like this:
# (x - 56000 )*0.55 + 39393 otherwise


# * Inheritance tax rates

def inheritanceTax_intended(x):
  return     (  0                          if x <  112337
    else     ( (x -  112337)*0.1           if x <  280884
      else   ( (x -  280884)*0.2  +  16855 if x < 2808436
        else ( (x - 2808436)*0.33 + 522365 ) ) ) )

def inheritanceTax_written(x):
  return     ( 0                           if x <  112337
    else     ( x            *0.1           if x <  280884
      else   ( (x -  280884)*0.2  +  28084 if x < 2808436
        else ( (x - 2808436)*0.25 + 533594 ) ) ) )


# * Wealth tax rates

def wealthTax_intended(x):
  return             (0                                if x <   84253
    else             ( (x -   84253)*0.01              if x <  140422
      else           ( (x -  140422)*0.015 + 561.69    if x <  280844
        else         ( (x -  280844)*0.02  + 2668.0198 if x <  702109
          else       ( (x -  702109)*0.025 + 11093.319 if x < 1404218
            else     ( (x - 1404218)*0.03  + 28646.043 if x < 2106327
              else   ( (x - 2106327)*0.035 + 49709.313 if x < 2808437
                else ( (x - 2808437)*0.04  + 74283.164 ) ) ) ) ) ) ) )

def wealthTax_written(x):
  return             (  0                            if x <   84253
    else             ( (x -    13500 )*0.01          if x <  140422
      else           ( (x -   140422 )*0.015 +  1269 if x <  280844
        else         ( (x -   280843 )*0.02  +  3376 if x <  702109
          else       ( (x -   969796 )*0.025 + 11801 if x < 1404218
            else     ( (x -  1685061 )*0.03  + 29354 if x < 2106327
              else   ( (x -  2106327 )*0.035 + 50417 if x < 2808437
                else ( (x - 14042183 )*0.04  + 74990 ) ) ) ) ) ) ) )


# Corporate income tax rates

def corpIncomeTax_intended(x):
  return         ( 0                                   if x < 1207628
    else         ( (x -     1207628)*0.04              if x < 2190581
      else       ( (x -     2190581)*0.045 + 39318.117 if x < 3454377
        else     ( (x -     3454377)*0.05  + 96188.94  if x < 1.7665066e7
          else   ( (x - 1.7665066e7)*0.055 + 806723.4  if x < 4.2126548e7
            else ( (x - 4.2126548e7)*0.06  + 2152105 ) ) ) ) ) )

def corpIncomeTax_written(x):
  return         ( 0                                     if x < 1207628
    else         ( (x -        145000)*0.04              if x < 2190581
      else       ( (x -       2190581)*0.045 + 39318.117 if x < 3454377
        else     ( (x -       3454377)*0.05  + 96188.94  if x < 1.7665066e7
          else   ( (x -   1.7665066e7)*0.055 + 806723.4  if x < 4.2126548e7
            else ( (x - 280843660)    *0.06  + 2152105 ) ) ) ) ) )


# Draw stuff

import matplotlib.pyplot as plt
import numpy as np

def linear( title, tax_base_name, function_name, function, xmin, xmax):
  x = np.arange(xmin, xmax, (xmax - xmin) / 10000)
  plt.plot( x,
            [function(a) for a in x] )
  plt.ylabel( "taxes (measured in UVTs)" )
  plt.xlabel(tax_base_name + ' in UVTs')
  plt.title(title)

def semilog_ratio( title, tax_base_name, function_name, function, xmin, xmax):
  x = np.arange(xmin, xmax, (xmax - xmin) / 10000)
  plt.semilogx( x,
                [function(a) / a for a in x] )
  plt.ylabel('fraction of ' + tax_base_name + ' lost to tax')
  plt.xlabel(tax_base_name + ' in UVTs')
  plt.title(title)

for (title,base,fname,f,xmin, xmax) in [
    ("Wealth tax formulas from the proposal",
     "wealth",      "written",  wealthTax_written,       0, 5e7),
    ("Wealth tax suggested by the proposal's rates and thresholds",
     "wealth",      "intended", wealthTax_intended,      0, 5e7),
    ( # Alternatively, this one can be treated specially,
      # to highlight a weird region, and zoom in on that region.
      # See the code below, tagged "huasidhuio20178590hsdjaklva",
      # for how to do that.
     "Inheritance tax formulas from the proposal",
     "inheritance", "written",  inheritanceTax_written,  0, 5e7),
    ("Inheritance tax suggested by the proposal's rates and thresholds",
     "inheritance", "intended", inheritanceTax_intended, 0, 5e7),
    ( "Inheritance tax formulas from the proposal",
      "corp-income", "written", corpIncomeTax_written, 0, 1e8),
    ( "Corporate income tax suggested by the proposal's rates and thresholds",
      "corp-income", "intended", corpIncomeTax_intended, 0, 1e8),
    ]:
  semilog_ratio( title, base,fname,f,xmin, xmax )
  plt.savefig( base + "-" + fname + "-" +
               str(xmin) + "-" + str(xmax) + ".png" )
  plt.close()

if False: # tag: huasidhuio20178590hsdjaklva
  for (title,base,fname,f,xmin, xmax) in [
          ( "Inheritance tax",  "inheritance", "written",
            inheritanceTax_written, 0, 5e7 ) ]:
    weird_min = 100000
    weird_max = 300000
    semilog_ratio( title, base, fname, f, xmin, xmax )
    plt.axvspan(weird_min, weird_max, color='red', alpha=0.5)
    plt.savefig( base + "-" + fname + "-" +
                 str(xmin) + "-" + str(xmax) + ".png" )
    plt.close()
    #
    g = lambda x : x - inheritanceTax_written(x)
    linear( "Inheritance received after taxes", "inheritance",
            "written, received", g, weird_min, weird_max )
    plt.savefig( base + "-" + fname + "-" + "linear" + "-" +
                 str(weird_min) + "-" + str(weird_max) + ".png" )
    plt.close()
