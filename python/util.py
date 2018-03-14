def printInRed(message):
    """from https://stackoverflow.com/a/287934/916142"""
    CSI="\x1B["
    print( CSI+"31;40m" + message + CSI + "0m")

def describeWithMissing(df):
  x = df.describe()
  y = []
  yy = pd.DataFrame( df.isnull().sum()
                     , columns = ["missing"]
                   ).transpose()
  return yy.append( x )
