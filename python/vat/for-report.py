util.describeWithMissing(purchases)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    util.describeWithMissing(people)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    util.describeWithMissing(households)

util.describeWithMissing(households)

for i in range(20):                                 
  pd.DataFrame( people["education"] ).quantile(i/20)

households["has-child"] = households["age-min"] < 18
dwmParamByGroup("vat/inc", "has-child",households)
dwmParamByGroup("vat/inc", "has-student", households)
households["has-elderly"] = households["age-max"] > 65
dwmParamByGroup("vat/inc","has-elderly",households)
dwmParamByGroup("vat/inc","edu-max",households)

vat / val by age (10-year bins)
val / inc by income decile
vat / val by income decile
