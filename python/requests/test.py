if True:
  from   datetime import datetime, timedelta
  import numpy as np
  import pandas as pd
  #
  import python.build.output_io as oio
  import python.common.common   as c
  import python.requests        as r


def test_memory_permits_another_run ():
    assert not r.memory_permits_another_run (
        gb_used = 5,
        constraints = { "max_gb" : 7,
                        "max_user_gb" : 3 } )
    assert     r.memory_permits_another_run (
        gb_used = 5,
        constraints = { "max_gb" : 7,
                        "max_user_gb" : 1 } )

def test_delete_oldest ():
  df = pd.DataFrame ( [ [ 1, 2, np.nan ],
                        [ 1, 1, np.nan ],
                        [ 3, 5, np.nan ],
                        [ 2, 4, np.nan ],
                        [ 2, 3, np.nan ] ],
                      columns = ["user", "requested", "completed"] )
  assert ( r.delete_oldest ( df )
         . reset_index ( drop = True )
         . equals (
           r.format_times (
             df . iloc [[4,2]]
             . reset_index ( drop = True ) ) ) )

def test_at_least_one_is_old ():
  constraints = { "min_survival_minutes" : 60 }
  now = datetime.now()
  early = now - timedelta (
      minutes = constraints [ "min_survival_minutes" ] * 2 )
  df = pd.DataFrame ( [ [ 1, 1, np.nan ],
                        [ 2, 2, now],
                        [ 3, 3, early ] ],
                      columns = ["user", "completed", "requested"] )
  assert not r.at_least_one_is_old ( df[:2]     , constraints )
  assert     r.at_least_one_is_old ( df         , constraints )
  assert     r.at_least_one_is_old ( df.iloc[2:], constraints )

def test_uniquify_requests ():
    cols = ["user","requested"]
    a = pd.DataFrame ( [], columns = cols )
    assert r.uniquify_requests (a) . equals (a)
    b = pd.DataFrame ( [ [ "", 0 ],
                         [ "a", 1 ],
                         [ "a", 2 ] ],
                      columns = cols )
    assert r.uniquify_requests (b) . equals ( b[:2] )

def test_unexecuted_requests_exist ():
    has_some = pd.DataFrame ( [ np.nan, 0 ],
                              columns = ["completed"] )
    has_none = pd.DataFrame ( [ np.nan, np.nan ],
                              columns = ["completed"] )
    assert     r.unexecuted_requests_exist( has_some )
    assert not r.unexecuted_requests_exist( has_none )

if True:
  test_memory_permits_another_run ()
  test_delete_oldest ()
  test_at_least_one_is_old ()
  test_uniquify_requests ()
  test_unexecuted_requests_exist ()
  #
  oio.test_write(
      1, # PTIFALL: Uses no data, so always writes to recip-1/
      "requests", "" )
