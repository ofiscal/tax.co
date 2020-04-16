if True:
  import datetime
  #
  from   python.common.misc import min_wage
  from   python.common.util import near
  import python.build.output_io as oio
  import python.build.ss_functions as sf
  import python.build.ss_schedules as ss


def test_mk_pension():
  contractor = True
  employee = False
  if True: # for contractors
    assert near( sf.mk_pension( contractor, 0.5 * min_wage ),
                 0 )
    assert near( sf.mk_pension( contractor, 2 * min_wage ),
                 0.16 * min_wage )
    assert near( sf.mk_pension( contractor, 10 * min_wage ),
                 0.16 * 4 * min_wage)
    assert near( sf.mk_pension( contractor, 200 * min_wage ),
                 0.16 * 25 * min_wage)
  
  if True: # for employees
    assert near( sf.mk_pension( employee, 0.5 * min_wage ),
                 0 )
    assert near( sf.mk_pension( employee, min_wage ),
                 0.04 *                   min_wage )
    assert near( sf.mk_pension( employee, 12 * min_wage ),
                 0.04 *                   12 * min_wage )
    assert near( sf.mk_pension( employee, 13 * min_wage ),
                 0.04 * 0.7 *             13 * min_wage )
    assert near( sf.mk_pension( employee, 50 * min_wage ),
                 0.04 *                   25 * min_wage )

if True:
  log = str( datetime.datetime.now() )
  test_mk_pension()
  oio.test_write( 1 # PITFALL: Doesn't use any subsample,
                    # so it's as if it's only tested on the full sample.
                , "build_ss_functions"
                , log )
