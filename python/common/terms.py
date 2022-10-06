# Hard-coding strings throughout the codebase is dangerous,
# as typos might go unnoticed, causing silent failure.
# Instead use the variables defined below,
# so that if one of them is written incorrectly, Python will let us know.


###########################
#### ### Strategies ### ###
###########################

# PITFALL: Whenever adding a strategy here,
# be sure to add it to valid_strategies as well.

# The default -- the law as of July 2022.
detail = "detail"

max_1340_uvt_deduction_and_max_4_dependents_72_uvt_each = \
  "max_1340_uvt_deduction_and_max_4_dependents_72_uvt_each"

# Here, dividends and ganancias ocasionales are taxed the same way
# as any other income, and the dedudctible limit is lower.
# The government proposed this on August 8 2022
single_cedula_with_single_1210_uvt_threshold = \
  "single_cedula_with_single_1210_uvt_threshold"

# Just like the status quo, except with a lower income tax deduction.
reduce_income_tax_deduction_to_1210_uvts = \
  "reduce_income_tax_deduction_to_1210_uvts"

valid_strategies = [ # There used to be a lot of these.
  # See the section on `retire-hypotheticals` in  `branches/branches.md`
  # for where they went.
  detail,
  max_1340_uvt_deduction_and_max_4_dependents_72_uvt_each,
  single_cedula_with_single_1210_uvt_threshold,
  reduce_income_tax_deduction_to_1210_uvts,
]
