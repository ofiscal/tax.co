if True: 
  re = regex.compile( ".*included in 6500.*" )
  inclusion_columns = [c for c in data.people.columns if re.match( c )]
  if data.people[ inclusion_columns ] . min() . min() != 0:
    print( "WARNING: Some inclusion variable has a minimum other than 0." )
  if data.people[ inclusion_columns ] . max() . max() != 1:
    print( "WARNING: Some inclusion variable has a maximum other than 1." )
