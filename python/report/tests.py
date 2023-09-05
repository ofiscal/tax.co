import python.report.defs     as defs
import python.build.output_io as oio


def test_fill_if_percentile ():
  assert defs.fill_if_percentile ( "duck-percentile", "2" ) == "02"
  assert defs.fill_if_percentile ( "percentile-duck", "2" ) == "2"

if True:
  log = "starting\n"
  test_fill_if_percentile ()
  oio.test_write (
    1, # Since these tests do not depend on sample size.
    "python.report.tests",
    log )
