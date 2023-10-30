if True:
  import datetime
  #
  import python.build.output_io as oio
  import python.build.ss.functions as sf
  import python.build.ss.schedules as ss
  from   python.common.misc import min_wage
  from   python.common.util import near
  import python.common.common as common


# TODO: Rather than using these, use named arguments in the function below.
# That clarity will cost some brevity but seems worth it.
contractor = True
employee = False

def test_mk_pension():
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

def test_mk_pension_employer():
  if True: # for contractors, always 0
    assert near( sf.mk_pension_employer( contractor, 0 ), 0 )
    assert near( sf.mk_pension_employer( contractor, 1000 * min_wage ), 0 )
  if True: # for employees
    assert near( sf.mk_pension_employer( employee, 0.5 * min_wage ), 0 )
    assert near( sf.mk_pension_employer( employee,   5 * min_wage ),
                 0.12                              * 5 * min_wage )
    assert near( sf.mk_pension_employer( employee,  20 * min_wage ),
                 0.12 * 0.7                       * 20 * min_wage )
    assert near( sf.mk_pension_employer( employee, 100 * min_wage ),
                 0.12 *                             25 * min_wage )

def test_mk_salud():
  if True: # contractors
    assert near( sf.mk_salud( contractor, 0 ),
                 0 )
    assert near( sf.mk_salud( contractor, 2 * min_wage ),
                 0.125 * min_wage )
    assert near( sf.mk_salud( contractor, 4 * min_wage ),
                 0.125 * 0.4 *            4 * min_wage )
    assert near( sf.mk_salud( contractor, 100 * min_wage ),
                 0.125 *                   25 * min_wage )
  if True: # employees
    assert near( sf.mk_salud( employee, 0.5 * min_wage ),
                 0 )
    assert near( sf.mk_salud( employee, min_wage ),
                 0.04 *                 min_wage )
    assert near( sf.mk_salud( employee, 12 * min_wage ),
                 0.04 *                 12 * min_wage )
    assert near( sf.mk_salud( employee, 13 * min_wage ),
                 0.04 * 0.7 *           13 * min_wage )
    assert near( sf.mk_salud( employee, 50 * min_wage ),
                 0.04 *                 25 * min_wage )

def test_mk_salud_employer():
  if True: # for contractors, always 0
    assert near( sf.mk_salud_employer( contractor, 0 ), 0 )
    assert near( sf.mk_salud_employer( contractor, 1000 * min_wage ), 0 )
  if True: # for employees
    assert near( sf.mk_salud_employer( employee, 0.5 * min_wage ), 0 )
    assert near( sf.mk_salud_employer( employee,   9 * min_wage ), 0 )
    assert near( sf.mk_salud_employer( employee,  20 * min_wage ),
                 0.085 * 0.7                    * 20 * min_wage )
    assert near( sf.mk_salud_employer( employee, 100 * min_wage ),
                 0.085                          * 25 * min_wage )

def test_mk_solidaridad():
  if True: # contractor
    assert near( sf.mk_solidaridad( contractor, 0 ), 0 )
    assert near( sf.mk_solidaridad( contractor, 3    * min_wage ), 0 )
    assert near( sf.mk_solidaridad( contractor, 5    * min_wage ),
                 0.01 * 0.4 *                   5    * min_wage )
    assert near( sf.mk_solidaridad( contractor, 15   * min_wage ),
                 0.01 * 0.4 *                   15   * min_wage )
    assert near( sf.mk_solidaridad( contractor, 16.5 * min_wage ),
                 0.012 * 0.4 *                  16.5 * min_wage )
    assert near( sf.mk_solidaridad( contractor, 17.5 * min_wage ),
                 0.014 * 0.4 *                  17.5 * min_wage )
    assert near( sf.mk_solidaridad( contractor, 18.5 * min_wage ),
                 0.016 * 0.4 *                  18.5 * min_wage )
    assert near( sf.mk_solidaridad( contractor, 19.5 * min_wage ),
                 0.018 * 0.4 *                  19.5 * min_wage )
    assert near( sf.mk_solidaridad( contractor, 21   * min_wage ),
                 0.02 * 0.4 *                   21   * min_wage )
    assert near( sf.mk_solidaridad( contractor, 100  * min_wage ),
                 0.02 *                          25  * min_wage )

  if True: # employee
    assert near( sf.mk_solidaridad( employee, 0 ), 0 )
    assert near( sf.mk_solidaridad( employee, 3    * min_wage ), 0 )
    assert near( sf.mk_solidaridad( employee, 5    * min_wage ),
                 0.01 *                       5    * min_wage )
    assert near( sf.mk_solidaridad( employee, 13.1 * min_wage ),
                 0.01 * 0.7 *                 13.1 * min_wage )
    assert near( sf.mk_solidaridad( employee, 16.5 * min_wage ),
                 0.012 * 0.7 *                16.5 * min_wage )
    assert near( sf.mk_solidaridad( employee, 17.5 * min_wage ),
                 0.014 * 0.7 *                17.5 * min_wage )
    assert near( sf.mk_solidaridad( employee, 18.5 * min_wage ),
                 0.016 * 0.7 *                18.5 * min_wage )
    assert near( sf.mk_solidaridad( employee, 19.5 * min_wage ),
                 0.018 * 0.7 *                19.5 * min_wage )
    assert near( sf.mk_solidaridad( employee, 21   * min_wage ),
                 0.02 * 0.7 *                 21   * min_wage )
    assert near( sf.mk_solidaridad( employee, 100  * min_wage ),
                 0.02 *                        25  * min_wage )

def test_mk_parafiscales_employer():
  if True: # for contractors, always 0
    assert near( sf.mk_parafiscales_employer( contractor, 0 ), 0 )
    assert near( sf.mk_parafiscales_employer( contractor, 1000 * min_wage ), 0 )
  if True: # for employees
    assert near( sf.mk_parafiscales_employer( employee, 0.5 * min_wage ), 0 )
    assert near( sf.mk_parafiscales_employer( employee,   9 * min_wage ), 0 )
    assert near( sf.mk_parafiscales_employer( employee,  20 * min_wage ),
                 0.05 * 0.7                            * 20 * min_wage )
    assert near( sf.mk_parafiscales_employer( employee, 100 * min_wage ),
                 0.05                                  * 25 * min_wage )

def test_mk_cajas_de_compensacion_employer():
  t = sf.mk_cajas_de_compensacion_employer
  if True: # for contractors, always 0
    assert near( t( contractor, 0 ), 0 )
    assert near( t( contractor, 1000 * min_wage ), 0 )
  if True: # for employees
    assert near( t( employee,  0.5 * min_wage ), 0 )
    assert near( t( employee,  1.1 * min_wage ),
                 0.04        * 1.1 * min_wage )
    assert near( t( employee,  12  * min_wage ),
                 0.04        * 12  * min_wage )
    assert near( t( employee,  20  * min_wage ),
                 0.04 * 0.7  * 20  * min_wage )
    assert near( t( employee, 100  * min_wage ),
                 0.04        * 25  * min_wage )

def test_mk_cesantias_y_primas_employer():
  t = sf.mk_cesantias_y_primas_employer
  if True: # for contractors, always 0
    assert near( t( contractor, 0 ), 0 )
    assert near( t( contractor, 1000 * min_wage ), 0 )
  if True: # for employees
    assert near( t( employee,  0.5 * min_wage ), 0 )
    assert near( t( employee,  1.1 * min_wage ),
                 (2.12 / 12) * 1.1 * min_wage )
    assert near( t( employee,  12  * min_wage ),
                 (2.12 / 12) * 12  * min_wage )
    assert near( t( employee,  14  * min_wage ), 0 )
    assert near( t( employee, 100  * min_wage ), 0 )


if True:
  log = str( datetime.datetime.now() )
  test_mk_pension()
  test_mk_pension_employer()
  test_mk_salud()
  test_mk_salud_employer()
  test_mk_solidaridad()
  test_mk_parafiscales_employer()
  test_mk_cajas_de_compensacion_employer()
  test_mk_cesantias_y_primas_employer()
  for vs in common . valid_subsamples:
    # PITFALL: Looping over subsample sizes because this program
    # doesn't use any data. If it works, it works for all subsamples.
    oio.test_write ( vs
                   , "build_ss_functions"
                   , log )
