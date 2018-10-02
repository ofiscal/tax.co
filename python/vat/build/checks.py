if True: # check the inclusion variables
  re = regex.compile( ".*included in 6500.*" )
  inclusion_columns = [c for c in data.people.columns if re.match( c )]
  if data.people[ inclusion_columns ] . min() . min() != 0:
    print( "WARNING: Some inclusion variable has a minimum other than 0." )
  if data.people[ inclusion_columns ] . max() . max() != 1:
    print( "WARNING: Some inclusion variable has a maximum other than 1." )

if True: # check that (after fillna()) no income variables are missing
  re = regex.compile( "income.*" )
  income_columns = [c for c in data.people.columns if re.match( c )]
  if data.people[ inclusion_columns ] . isnull() . any() . any():
    print( "WARNING: Some income variable is still NaN (after calling fillna())."
