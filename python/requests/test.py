if True:
  from   datetime import datetime, timedelta
  import numpy as np
  import pandas as pd
  #
  import python.build.output_io as oio
  import python.common.common   as c
  import python.requests.lib    as r


def test_memory_permits_another_run ():
    assert not r.memory_permits_another_run (
        gb_used = 5,
        constraints = { "max_gb" : 7,
                        "max_user_gb" : 3 } )
    assert     r.memory_permits_another_run (
        gb_used = 5,
        constraints = { "max_gb" : 7,
                        "max_user_gb" : 1 } )

def test_delete_oldest_request ():
  columns = [ "user email", "user", "completed",
              "time requested", "time completed" ]
  df = pd.DataFrame ( [ [ 1, 1, False, 0, 0 ],
                        [ 2, 2, True, 1, 1 ] ],
                      columns = columns )
  assert ( r.delete_oldest_request ( df )
           # Even though user 2's request was issued second,
           # it is the first completed one, so it is the one dropped.
           . equals ( r.format_times ( df[:1] ) ) )
  df = pd.DataFrame ( [ [ 1, 1, True, 2, np.nan ],
                        [ 1, 1, True, 1, np.nan ],
                        [ 3, 3, True, 5, np.nan ],
                        [ 2, 2, True, 4, np.nan ],
                        [ 2, 2, True, 3, np.nan ] ],
                      columns = columns )
  assert ( r.delete_oldest_request ( df )
         . reset_index ( drop = True )
         . equals (
           r.format_times (
             df . iloc [[4,2]]
             . reset_index ( drop = True ) ) ) )

def test_at_least_one_result_is_old ():
  constraints = { "min_survival_minutes" : 60 }
  now = datetime.now ()
  early = now - timedelta (
      minutes = constraints [ "min_survival_minutes" ] * 2 )
  df = pd.DataFrame (
     [ [ 1, 1, False, early, np.nan ],  # unfinished
       [ 2, 2, True,  now, now],        # finished but young
       [ 3, 3, True,  early, early ] ], # finished and old
     columns = [ "user email", "user", "completed",
                 "time requested","time completed" ] )
  assert not r.at_least_one_result_is_old ( df[:2]     , constraints )
  assert     r.at_least_one_result_is_old ( df         , constraints )
  assert     r.at_least_one_result_is_old ( df.iloc[2:], constraints )

def test_uniquify_requests ():
    cols = [ "user email", "user", "completed",
             "time requested", "time completed" ]
    a = pd.DataFrame ( [], columns = cols )
    assert r.uniquify_requests (a) . equals (a)
    b = pd.DataFrame ( [
        [ "" , "" , False, np.nan, np.nan ],
        [ "" , "" , False, np.nan, np.nan ],
        [ "0", "0", False, 0     , 0      ],
        [ "0", "0", False, np.nan, np.nan ],
        [ "a", "a", True,  0     , 0      ],
        [ "a", "a", False, 0     , 0      ],
        [ "b", "b", True,  1     , 1      ],
        [ "b", "b", True,  0     , 0      ],
        [ "c", "c", True,  0     , 0      ],
        [ "c", "c", True,  1     , 1      ],
        [ "c", "c", True,  0     , 0      ],
        ],
     columns = cols )
    assert r.uniquify_requests (b) . equals (
        pd.DataFrame (
            [ [ "",  "",  False, np.nan, np.nan ],
              [ "0", "0", False, 0     , 0      ],
              [ "a", "a", False, 0     , 0      ],
              [ "a", "a", True , 0     , 0      ],
              [ "b", "b", True , 0     , 0      ],
              [ "c", "c", True , 0     , 0      ], ],
        columns = cols ) )

def test_unexecuted_requests_exist ():
    def go ( s ):
        return r.unexecuted_requests_exist (
            pd.DataFrame ( s,
                           columns = ["completed"] ) )
    assert     go ( [ False, True  ] )
    assert     go ( [ False, False ] )
    assert not go ( [ True,  True  ] )

def test_next_request ():
    cols = [ "user email", "user", "completed",
             "time completed","time requested" ]
    df = pd.DataFrame (
      [ [ "1", "1", False, 99, 99 ],
        [ "2", "2", False, 6,  6 ],
        [ "3", "3", True,  7,  7 ],
        [ "4", "4", True,  8,  8 ], ],
      columns = cols )
    assert r.next_request ( df ) == "2"

if True:
  test_memory_permits_another_run ()
  test_delete_oldest_request ()
  test_at_least_one_result_is_old ()
  test_uniquify_requests ()
  test_unexecuted_requests_exist ()
  test_next_request ()
  #
  oio.test_write(
      1, # PTIFALL: Uses no data, so always writes to recip-1/
      "requests", "" )
