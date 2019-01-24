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

people["pension"] = people.apply(
    lambda row: mk_pension(          row["independiente"], row["income, labor, cash"] )
  , axis = "columns" )
people["pension, employer"] = people.apply(
    lambda row: mk_pension_employer( row["independiente"], row["income, labor, cash"] )
  , axis = "columns" )

oio.saveStage( c.subsample
             , people
             , 'people_4_ss.' + c.vat_strategy_suffix
)
