# These functions use the schedules encoded at
# `python/build/ss_schedules.py` to compute someone's
# "generalized income taxes" (a term I am inventing,
# which include things like social security contributions,
# which is not technically a tax).

if True:
  import pandas                    as pd
  #
  import python.build.ss.schedules as ss
  import python.common.util        as util


def mk_arl ( independiente, income ):
  if independiente:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contrib_schedule_for_contractor["ARL"] )
    return compute_base ( income ) * rate
  else: return 0

def mk_arl_employer ( independiente, income ):
  if independiente: return 0
  else:
    (_, compute_base, rate) = util.tuple_by_threshold (
        income, ss.ss_contribs_by_employer [ "ARL"] )
    return compute_base ( income ) * rate

def mk_aux_transporte_employer ( independiente, income ):
  if independiente: return 0
  else:
    (_, compute_base, rate) = util.tuple_by_threshold (
        income, ss.ss_contribs_by_employer [ "aux transporte"] )
    return compute_base ( income ) * rate

def mk_cajas_de_compensacion_employer( independiente, income ):
  if independiente: return 0
  else:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contribs_by_employer["cajas de compensacion"] )
    return compute_base( income ) * rate

def mk_cesantias_y_primas_employer( independiente, income ):
  if independiente: return 0
  else:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contribs_by_employer["cesantias + primas"] )
    return compute_base( income ) * rate

def mk_parafiscales_employer( independiente, income ):
  if independiente: return 0
  else:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contribs_by_employer["parafiscales"] )
    return compute_base( income ) * rate

def mk_pension( independiente, income ):
  if independiente:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contrib_schedule_for_contractor["pension"] )
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
  else:
    (_, compute_base, rate) = util.tuple_by_threshold(
        income, ss.ss_contrib_schedule_for_employee["solidaridad"] )
  return compute_base( income ) * rate

def mk_vacaciones_employer ( independiente, income ):
  if independiente: return 0
  else:
    (_, compute_base, rate) = util.tuple_by_threshold (
        income, ss.ss_contribs_by_employer [ "vacaciones"] )
    return compute_base ( income ) * rate

ss_tax_names_and_recipes = \
  [ ( "tax, ss, ARL",
      mk_arl)
  , ( "tax, ss, ARL, employer",
      mk_arl_employer)
  , ( "tax, ss, aux transporte, employer",
      mk_aux_transporte_employer)
  , ( "tax, ss, cajas de compensacion", # PITFALL: nominally from the employer
      mk_cajas_de_compensacion_employer)
  , ( "cesantias + primas",             # PITFALL: nominally from the employer
      mk_cesantias_y_primas_employer)   # PITFALL: not a tax -- that's why its
                                        # name looks different.
  , ( "tax, ss, parafiscales",          # PITFALL: nominally from the employer
      mk_parafiscales_employer)
  , ( "tax, ss, pension",
      mk_pension)
  , ( "tax, ss, pension, employer",
      mk_pension_employer)
  , ( "tax, ss, salud",
      mk_salud)
  , ( "tax, ss, salud, employer",
      mk_salud_employer)
  , ( "tax, ss, solidaridad",
      mk_solidaridad)
  , ( "vacaciones, employer",
      mk_vacaciones_employer) ] # PITFALL: not a tax -- that's why its
                                # name looks different.

def mk_ss_contribs( ppl : pd.DataFrame ) -> pd.DataFrame:
  """PITFALL: Destructive."""
  for (goal,function) in ss_tax_names_and_recipes:

    ppl[goal] = ppl.apply(
        lambda row: function(
            row["independiente"],
            row["income, labor, cash"] )
      , axis = "columns" )

  ppl["tax, ss, total employee contribs"] = \
    ( ppl["tax, ss, ARL"]
    + ppl["tax, ss, pension"]
    + ppl["tax, ss, salud"]
    + ppl["tax, ss, solidaridad"] )

  ppl["tax, ss"] = (
    ppl [ [ name for (name, _)
            in ss_tax_names_and_recipes ] ]
    . sum ( axis = "columns" ) )

  return ppl
