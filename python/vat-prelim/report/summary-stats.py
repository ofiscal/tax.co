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
util.describeWithMissing( households [["vat/income"]] )
util.describeWithMissing(
  households [ households["value/inc"] !=  np.inf ] [["value/inc"]]
)

util.dwmParamByGroup("vat/income", "has-child",households).round(3)
util.dwmParamByGroup("vat/income", "has-child",
                     households [ households["vat/income"] < np.inf ] ).round(3)
util.dwmParamByGroup("vat/income", "has-child",
                     households [ households["income"] > 0 ] ).round(3)

util.dwmParamByGroup("vat/income", "has-student", households)
util.dwmParamByGroup("vat/income", "has-child",
                     households [ households["income"] > 0 ] ).round(3)

util.dwmParamByGroup("vat/income","has-elderly",households)
util.dwmParamByGroup("vat/income", "has-elderly",
                     households [ households["income"] > 0 ] ).round(3)

util.dwmParamByGroup("vat/income","edu-max",households)
util.dwmParamByGroup("vat/income","edu-max",
                     households [ households["income"] > 0 ] ).round(3)


# Individual spending and taxes
util.dwmParamByGroup("vat/income","age-decile",people)
util.dwmParamByGroup("vat/income","age-decile",
                     people[ people["income"] > 0 ] )
util.dwmParamByGroup("value/inc","age-decile",
                     people[ people["income"] > 0 ] )

util.dwmParamByGroup("vat/income","income-decile",people)
util.dwmParamByGroup("vat/income","income-decile",
                     people[ people["vat/income"] < np.inf ] )

util.dwmParamByGroup("vat/income","race",
                     people[ people["income"] > 0 ] )

util.dwmParamByGroup("vat/income","female",
                     people[ people["income"] > 0 ] )
