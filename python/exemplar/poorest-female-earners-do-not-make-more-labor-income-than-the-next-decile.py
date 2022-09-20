# PURPOSE:
# Daniel found that the poorest decile in the female earners data
# had a mean labor income orders of magnitude greater than
# the next (richer!) decile.
# I was unable to repeat the finding,
# and suspect it may be due to .xlsx format confusions.
# I responded by having the sim email both .xlsx and .csv results,
# not just .xlsx.
#
# NOTE: Income quantiles are defined for earners as a whole,
# without regard to gender, based on total income rather than labor income.
# Only after that are females and males broken out.


# HOW TO USE THIS CODE:
# First run var_summaries_by_group.py until earnersFemale is created.
# THen:

ef = earnersFemale.copy()

ef_first = ef.iloc[0]
for i in ef_first.index:
  print( i, " : ", str( ef_first[i] ) )

# del(ef_d0,ef_d1,ef_d_gt1)

# Define decile 0 and deciles greater than 0
ef_d0    = ef [ ef["income-decile"] == 0 ]
ef_d1    = ef [ ef["income-decile"] == 1 ]
ef_d_gt1 = ef [ ef["income-decile"] >  1 ]

# Verify those two things form a partition
all ( [ len(ef_d0)    > 0
      , len(ef_d1)    > 0
      , len(ef_d_gt1) > 0
      , len(ef_d0) + len(ef_d1) + len(ef_d_gt1) == len(ef) ] )

# Verify some threshold separates incomes in the two partitions.
# (Of course, many thresholds do, although their measure is small.)
max_of_d0    = ef_d0    ["income"].max()
min_of_d1    = ef_d1    ["income"].min()
max_of_d1    = ef_d1    ["income"].max()
min_of_d_gt1 = ef_d_gt1 ["income"].min()
all ( [ max_of_d0 < min_of_d1,
        max_of_d1 < min_of_d_gt1 ] )

ef_d0    ["income, labor"] . describe()
ef_d1    ["income, labor"] . describe()
ef_d_gt1 ["income, labor"] . describe()
