import numpy                        as np
import pandas                       as pd
import python.build.classes         as classes
import python.build.names_in_tables as n
import python.common.misc           as c
import python.common.cl_args        as cl


edu_key = {
    1 : n.edu_vals.nada
  , 2 : n.edu_vals.pre
  , 3 : n.edu_vals.pri
  , 4 : n.edu_vals.sec
  , 5 : n.edu_vals.med
  , 6 : n.edu_vals.sup
  , 9 : n.edu_vals.no_sabe
}

race_key = {
    1 : n.race_vals.ind
  , 2 : n.race_vals.git
  , 3 : n.race_vals.raiz
  , 4 : n.race_vals.pal
  , 5 : n.race_vals.neg
  , 6 : n.race_vals.nada
}

demog = {
    "P6050" : n.relationship
  , "P6020" : n.female
  , "P6040" : n.age
  , "P6080" : n.race
  , "P5170" : n.pre_k_or_daycare
  , "P6060" : n.skipped_3_meals
  , "P6160" : n.literate
  , "P6170" : n.student
  , "P6210" : n.edu
  , "P6310" : n.why_not_seek_work
  , "P6430" : n.independiente
}

work = { "P6920"   : n.pension_contributing_pre
       , "P6920S1" : n.pension_contribution_amount
       , "P6940"   : n.pension_contributors_pre
       , "P6990"   : n.seguro_laborales
}

income_govt = {
    "P9460S1"   : n.income_month_govt_unemployment
  , "P1668S1A1" : n.income_year_govt_familias_en_accion
  , "P1668S3A2" : n.income_year_govt_familias_en_su_tierra
  , "P1668S4A2" : n.income_year_govt_jovenes_en_accion
  , "P1668S2A2" : n.income_year_govt_programa_de_adultos_mayores
  , "P1668S5A2" : n.income_year_govt_transferencias_por_victimizacion
  , "P1668S1A4" : n.income_year_govt_familias_en_accion_in_kind
  , "P1668S3A4" : n.income_year_govt_familias_en_su_tierra_in_kind
  , "P1668S4A4" : n.income_year_govt_jovenes_en_accion_in_kind
  , "P1668S2A4" : n.income_year_govt_programa_de_adultos_mayores_in_kind
  , "P1668S5A4" : n.income_year_govt_transferencias_por_victimizacion_in_kind
}

income_labor = {
    "P6500"   : n.income_month_labor_formal_employment
  , "P7070"   : n.income_month_labor_job_2
  , "P7472S1" : n.income_month_labor_as_inactive
  , "P7422S1" : n.income_month_labor_as_unemployed
  , "P6750"   : n.income_month_labor_independent
  , "P6760"   : n.income_month_labor_independent_months
                   # divide P6750 by this to get monthly
                   # hopefully this is usually 1 or missing

  # below, in the variable `inclusion_pairs`, these are grouped
  , "P1653S1A1"  : n.income_month_labor_bonus_2
  , "P1653S1A2"  : n.income_month_labor_bonus_2_included_in_6500
  , "P1653S2A1"  : n.income_month_labor_bonus
  , "P1653S2A2"  : n.income_month_labor_bonus_included_in_6500
  , "P6585S3A1"  : n.income_month_labor_familiar
  , "P6585S3A2"  : n.income_month_labor_familiar_included_in_6500
  , "P6585S1A1"  : n.income_month_labor_food
  , "P6585S1A2"  : n.income_month_labor_food_included_in_6500
  , "P1653S4A1"  : n.income_month_labor_gastos_de_representacion
  , "P1653S4A2"  : n.income_month_labor_gastos_de_representacion_included_in_6500
  , "P6510S1"    : n.income_month_labor_overtime
  , "P6510S2"    : n.income_month_labor_overtime_included_in_6500
  , "P6585S2A1"  : n.income_month_labor_transport
  , "P6585S2A2"  : n.income_month_labor_transport_included_in_6500
  , "P1653S3A1"  : n.income_month_labor_viaticum
  , "P1653S3A2"  : n.income_month_labor_viaticum_included_in_6500

  , "P6779S1"    : n.income_month_labor_viaticum_2

  , "P550"       : n.income_year_labor_rural
  , "P6630S5A1"  : n.income_year_labor_bonus
  , "P6630S2A1"  : n.income_year_labor_christmas_bonus
  , "P6630S1A1"  : n.income_year_labor_prima_de_servicios
  , "P6630S3A1"  : n.income_year_labor_vacation_bonus
  , "P6630S4A1"  : n.income_year_labor_viaticum_3
  , "P6630S6A1"  : n.income_year_labor_work_accident_payments

  , "P6590S1"    : n.income_month_labor_food_in_kind
  , "P6600S1"    : n.income_month_labor_lodging_in_kind
  , "P6620S1"    : n.income_month_labor_other_in_kind
  , "P6610S1"    : n.income_month_labor_transport_in_kind
}

income_edu = {
    "P8610S2"    : n.income_year_edu_beca_in_kind
  , "P8612S2"    : n.income_year_edu_non_beca_in_kind
  , "P8610S1"    : n.income_year_edu_beca
  , "P8612S1"    : n.income_year_edu_non_beca
}

income_private = {
    "P7500S3A1"  : n.income_month_private_alimony
  , "P7510S3A1"  : n.income_year_private_from_private_domestic_firms
  , "P7510S4A1"  : n.income_year_private_from_private_foreign_firms
  , "P7510S1A1"  : n.income_year_private_remittance_domestic
  , "P7510S2A1"  : n.income_year_private_remittance_foreign
}

income_infrequent = {
    "P7513S9A1"  : n.income_year_infrequent_gambling
  , "P7513S10A1" : n.income_year_infrequent_inheritance
  , "P7513S8A1"  : n.income_year_infrequent_jury_awards
  , "P7513S12A1" : n.income_year_infrequent_refund_other
  , "P7513S11A1" : n.income_year_infrequent_refund_tax
}

income_capital = {
    "P7510S10A1" : n.income_year_investment_dividends
  , "P7510S5A1"  : n.income_year_investment_interest

  , "P7513S6A1"  : n.income_year_repayment_by_bank
  , "P7513S7A1"  : n.income_year_repayment_by_other
  , "P7513S5A1"  : n.income_year_repayment_by_person

  , "P7500S1A1"  : n.income_month_rental_real_estate_developed
  , "P7500S4A1"  : n.income_month_rental_real_estate_undeveloped
  , "P7500S5A1"  : n.income_month_rental_vehicle_or_equipment

  # These two variables record the same information. At least one is always zero.
  # (See python/test/stock_var_non_overlap.py for a proof.)
  # A person's income from sale of stock = their maximum = their sum.
  , "P7510S9A1"  : n.income_year_sale_stock
  , "P7513S4A1"  : n.income_year_sale_stock_2

  , "P7513S3A1"  : n.income_year_sale_livestock
  , "P7513S1A1"  : n.income_year_sale_real_estate
  , "P7513S2A1"  : n.income_year_sale_vehicle_or_equipment
}

income = { **income_govt
         , **income_labor
         , **income_edu
         , **income_private
         , **income_infrequent
         , **income_capital
         , "P7500S2A1"  : n.income_month_pension_age_or_illness
         , "P7510S6A1"  : n.income_year_cesantia
}

beca_sources_govt = {
    "P6207M2"  : n.beca_from_ICETEX
  , "P6207M3"  : n.beca_from_govt_central
  , "P6207M4"  : n.beca_from_govt_peripheral
  , "P6207M5"  : n.beca_from_another_public_entity
  , "P6207M6"  : n.beca_from_empresa_publica_familiar
}

beca_sources_private = {
    "P6207M1"  : n.beca_from_same_school
  , "P6207M7"  : n.beca_from_empresa_privada_familiar
  , "P6207M8"  : n.beca_from_other_private
  , "P6207M9"  : n.beca_from_organismo_internacional
  , "P6207M10" : n.beca_from_Universidades_y_ONGs
}

inclusion_pairs = [
     ( n.income_month_labor_bonus_2
     , n.income_month_labor_bonus_2_included_in_6500
  ), ( n.income_month_labor_bonus
     , n.income_month_labor_bonus_included_in_6500
  ), ( n.income_month_labor_familiar
     , n.income_month_labor_familiar_included_in_6500
  ), ( n.income_month_labor_food
     , n.income_month_labor_food_included_in_6500
  ), ( n.income_month_labor_gastos_de_representacion
     , n.income_month_labor_gastos_de_representacion_included_in_6500
  ), ( n.income_month_labor_overtime
     , n.income_month_labor_overtime_included_in_6500
  ), ( n.income_month_labor_transport
     , n.income_month_labor_transport_included_in_6500
  ), ( n.income_month_labor_viaticum
     , n.income_month_labor_viaticum_included_in_6500
  ) ]

files = [
  classes.File( "people"
    , "Caracteristicas_generales_personas.csv"
    , { **c.variables
      , **demog
      , **work
      , **income
      , **beca_sources_govt
      , **beca_sources_private
      , "P6236" : n.non_beca_sources
    } , c.corrections
      + [classes.Correction.Drop_Column( "file-origin" )
        ]
) ]

def count_public(list_as_str):
  """Count public sources of funding in the "non-beca sources" variable."""
  stripped = list_as_str . strip()
  if stripped in [np.nan, ""]: return 0
  else:
    num_list = map( float
                  , stripped . split(" ") )
    sources = filter( lambda x: x in [2,3,4], num_list )
    return len( list( sources ) )

# count private sources of funding in the "non-beca sources" variable
def count_private(list_as_str):
  stripped = list_as_str . strip()
  if stripped in [np.nan, ""]: return 0
  else:
    num_list = map( float
                  , stripped . split(" ") )
    sources = filter( lambda x: not x in [2,3,4], num_list )
    return len( list( sources ) )
