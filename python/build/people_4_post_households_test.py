if True:
  import datetime
  import pandas as pd
  #
  from   python.common.misc import num_people
  import python.build.output_io as oio
  import python.common.common   as com


if True:
  log = ( str( datetime.datetime.now() )
          + "\nThis is a test." )

  # unit tests
  # test_insert_has_dependent_column()

  # integration tests
  # ps = oio.readStage ( ...
  # assert ...

  oio.test_write( com.subsample
                , "people_4_post_households"
                , log )
