import os

import python.common.common      as c


process_marker_path = os.path.join ( c.tax_co_root,
                                     "data/request-ongoing" )
users_path          = os.path.join ( c.tax_co_root,
                                     "users/" )
constraints_path    = os.path.join ( c.tax_co_root,
                                     "data/constraints-time-memory.json" )
requests_path       = os.path.join ( c.tax_co_root,
                                     "data/requests.csv" )
requests_temp_path  = os.path.join ( c.tax_co_root,
                                     "data/requests.temp.csv" )
global_log_path     = os.path.join ( c.tax_co_root,
                                     "requests-log.txt" )

# This explains what the simulation results are.
email_body = """
Los resultados de la microsimulación que usted pidió son los archivos .zip adjuntos. (Si todo salió bien, el adjunto archivo `logs.zip` no le va a importar.)

(If someone wants to translate the rest of this into Spanish, please do ;)

When the simulation runs, it computes what would happen under the user's (your) specified tax scenario, and compares that to what would happen under the baseline scenario, which is our model of the current legal reality. The results include files whose names follow one of the forms "report*.csv", "change-in*by*.png", and "changes_*.csv".

Each "report" spreadsheet describes the user's scenario. At the top of each column is a label indicating the group that that column describes. At the far left of each row is a label indicating what statistic -- average income, for instance -- that row describes. The reports differ in the unit of observation of the underlying dataset that the report describes:

  earners                         = people who could make money
  nonzero_earners_by_labor_income = people who *do* make money
  earnersMale                     = male earners
  earnersFemale                   = female earners
  households                      = households
  householdsFemale                = female households
  householdsMale                  = male households
  households_by_IT_per_capita     = households

The reports *also* differ in the variable used to compute income quantiles (deciles, percentiles and milliles). In general, the household-level data sets compute quantiles from DANE's "IT", whereas the individual-level data sets compute it from our own (total individual) "income" aggregate. But there are two exceptions: In `households_by_IT_per_capita`, the quantiles are of "IT per capita", and in `nonzero_earners_by_labor_income` they are of "income, labor".

The reports with "tmi" ("too much information") data sets include every row we report. The other reports include only a selection of those rows we tend to care most about.

Once you know what all that stuff is, the "change*" data sets are hopefully self-explanatory.
"""
