# Overview of the three data sets
util.compareDescriptives( {'purchases' : purchases} )

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    util.describeWithMissing(people)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    util.describeWithMissing(households)


# Education quantiles
  # see "qcut" below for a better way to do this kind of thing
for i in range(20):                                 
  pd.DataFrame( people["education"] ).quantile(i/20)


# Household spending and taxes
util.describeWithMissing( households [["value/inc"]] )
util.describeWithMissing( households [["vat/inc"]] )
util.describeWithMissing(
  households [ households["value/inc"] !=  np.inf ] [["value/inc"]]
)

util.dwmParamByGroup("vat/inc", "has-child",households).round(3)
util.dwmParamByGroup("vat/inc", "has-child",
                     households [ households["vat/inc"] < np.inf ] ).round(3)
util.dwmParamByGroup("vat/inc", "has-child",
                     households [ households["income"] > 0 ] ).round(3)

util.dwmParamByGroup("vat/inc", "has-student", households)
util.dwmParamByGroup("vat/inc", "has-child",
                     households [ households["income"] > 0 ] ).round(3)

util.dwmParamByGroup("vat/inc","has-elderly",households)
util.dwmParamByGroup("vat/inc", "has-elderly",
                     households [ households["income"] > 0 ] ).round(3)

util.dwmParamByGroup("vat/inc","edu-max",households)
util.dwmParamByGroup("vat/inc","edu-max",
                     households [ households["income"] > 0 ] ).round(3)


# Individual spending and taxes
util.dwmParamByGroup("vat/inc","age-decile",people)
util.dwmParamByGroup("vat/inc","age-decile",
                     people[ people["income"] > 0 ] )
util.dwmParamByGroup("value/inc","age-decile",
                     people[ people["income"] > 0 ] )

util.dwmParamByGroup("vat/inc","income-decile",people)
util.dwmParamByGroup("vat/inc","income-decile",
                     people[ people["vat/inc"] < np.inf ] )

util.dwmParamByGroup("vat/inc","race",
                     people[ people["income"] > 0 ] )

util.dwmParamByGroup("vat/inc","female",
                     people[ people["income"] > 0 ] )
