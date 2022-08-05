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

attachments = [
  "report_households.detail.2019.xlsx",
  "report_households_tmi.detail.2019.xlsx",
  "report_earners.detail.2019.xlsx",
  "report_earners_tmi.detail.2019.xlsx",
  "change-in.tax-mean.by-households.detail.2019.png",
  "change-in.tax-mean.by-earners.detail.2019.png",
  "../..", "logs.zip",
]
