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

