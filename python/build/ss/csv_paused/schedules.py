""" The SS schedules are defined in code, in the file
  python/build/ss/schedules.py
That idiom is hostile to the interactive online model,
in which users define their own parameters.

To facilitate that,
in 2022 I started refactoring that program
using the new idiom in this program,
so that SS schedules would be represented as CSV files.

`./equivalence_test.py` includes tests to ensure that the two idioms are equivalent.

Our priorities then changed, and I have not finished the conversion.
"""

import os
import pandas as pd
from   typing import Callable, Dict
#
from   python.build.ss.myTypes import AverageTaxSchedule
from   python.common.misc import min_wage


def average_tax_function (
    fraction_of_wage      : float, # fraction of wage taxed
    min_base_in_min_wages : float, # minimum wage assumed
    max_base_in_min_wages : float  # maximum wage taxed
) -> Callable [ [float], float ]: # computes taxable base from wage
  return ( lambda wage:
           min ( max ( wage     * fraction_of_wage,
                       min_wage * min_base_in_min_wages ),
                 min_wage       * max_base_in_min_wages ) )

def ss_tax_schedule_from_frame (
    df : pd.DataFrame
) ->  AverageTaxSchedule:
  df["lambda"] = df.apply (
    lambda row: average_tax_function (
      row["fraction_of_wage"],
      row["min_base_in_min_wages"],
      row["max_base_in_min_wages"] ),
    axis = "columns" )
  df["min_threshold"] = df["min_threshold_in_min_wages"] * min_wage
  return ( df [[ "min_threshold",
                 "lambda",
                 "average_tax_rate" ]]
           . values . tolist () )

def ss_tax_schedule_from_csv (
    basename : str,
) -> AverageTaxSchedule:
  return ss_tax_schedule_from_frame (
    pd.read_csv (
      os.path.join ( "data/ss/",
                     basename + ".csv") ) )

ss_contrib_schedule_for_contractor_new : \
  Dict [ str, AverageTaxSchedule ] = {
    "pension"     : ss_tax_schedule_from_csv ( "contractor_pension"     ),
    "salud"       : ss_tax_schedule_from_csv ( "contractor_salud"       ),
    "solidaridad" : ss_tax_schedule_from_csv ( "contractor_solidaridad" ), }

ss_contrib_schedule_for_employee_new : \
  Dict [ str, AverageTaxSchedule ] = {
    "pension"     : ss_tax_schedule_from_csv ( "employee_pension"     ),
    "salud"       : ss_tax_schedule_from_csv ( "employee_salud"       ),
    "solidaridad" : ss_tax_schedule_from_csv ( "employee_solidaridad" ), }

# For employees, but not contractors,
# some contributions are also made by the employer.
ss_contribs_by_employer_new : \
  Dict [ str, AverageTaxSchedule ] = {
    "pension"               : ss_tax_schedule_from_csv ( "employer_pension"               ),
    "cajas de compensacion" : ss_tax_schedule_from_csv ( "employer_cajas_de_compensacion" ),
    "cesantias + primas"    : ss_tax_schedule_from_csv ( "employer_cesantias_y_primas"    ),
    "parafiscales"          : ss_tax_schedule_from_csv ( "employer_parafiscales"          ),
    "salud"                 : ss_tax_schedule_from_csv ( "employer_saluid"                ), }
