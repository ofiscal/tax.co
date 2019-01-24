import sys
import pandas                    as pd

import python.build.ss_schedules as ss
import python.build.output_io    as oio
import python.util               as util
import python.build.common       as c


people = oio.readStage( c.subsample
                      , "people_3_purchases." + c.vat_strategy_suffix )

people["4 por mil"] = 0.004 * (people["income, cash"] - 11.6e6)

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

for (goal,function) in [
      ("tax, pension", mk_pension)
    , ("tax, pension, employer", mk_pension_employer)
    , ("tax, salud", mk_salud)
    , ("tax, salud, employer", mk_salud_employer)
    , ("tax, solidaridad", mk_solidaridad)
    , ("tax, parafiscales", mk_parafiscales_employer)
    , ("tax, cajas de compensacion", mk_cajas_de_compensacion_employer)
    , ("tax, cesantias", mk_cesantias_employer) ]:
  people[goal] = people.apply(
      lambda row: function( row["independiente"], row["income, labor, cash"] )
    , axis = "columns" )

oio.saveStage( c.subsample
             , people
             , 'people_4_ss.' + c.vat_strategy_suffix
)
