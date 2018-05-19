## Household spending and taxes / by income

households["income-decile"] = pd.qcut(
  households["income"], 10, labels = False, duplicates='drop')
  # duplicates='drop' is important; it causes the ~47% of households
  # with zero income to be lumped into a single quantile
households["one"] = 1
counts = households.groupby( "income-decile" )[["one"]] \
       .agg('sum').rename(columns = {"one":"count"})
mins = households.groupby( "income-decile" )[["income"]] \
       .agg('min').rename(columns = {"income":"min"})
maxs = households.groupby( "income-decile" )[["income"]] \
       .agg('max').rename(columns = {"income":"max"})
decile_summary = pd.concat([counts,mins,maxs],axis=1)
