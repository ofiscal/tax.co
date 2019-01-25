import pandas                    as pd

import python.build.ss_schedules as ss
import python.util               as util


def mk_pension( independiente, income ):
  if independiente:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contrib_schedule_for_contractor["pension"] )
    return compute_base( income ) * rate
  else:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contrib_schedule_for_employee["pension"] )
    return compute_base( income ) * rate

def mk_pension_employer( independiente, income ):
  if independiente: return 0
  else:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contribs_by_employer["pension"] )
    return compute_base( income ) * rate

def mk_salud( independiente, income ):
  if independiente:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contrib_schedule_for_contractor["salud"] )
    return compute_base( income ) * rate
  else:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contrib_schedule_for_employee["salud"] )
    return compute_base( income ) * rate

def mk_salud_employer( independiente, income ):
  if independiente: return 0
  else:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contribs_by_employer["salud"] )
    return compute_base( income ) * rate

def mk_solidaridad( independiente, income ):
  if independiente:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contrib_schedule_for_contractor["solidaridad"] )
    return compute_base( income ) * rate
  else:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contrib_schedule_for_employee["solidaridad"] )
    return compute_base( income ) * rate

def mk_parafiscales_employer( independiente, income ):
  if independiente: return 0
  else:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contribs_by_employer["parafiscales"] )
    return compute_base( income ) * rate

def mk_cajas_de_compensacion_employer( independiente, income ):
  if independiente: return 0
  else:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contribs_by_employer["cajas de compensacion"] )
    return compute_base( income ) * rate

def mk_cesantias_employer( independiente, income ):
  if independiente: return 0
  else:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contribs_by_employer["cesantias"] )
    return compute_base( income ) * rate
