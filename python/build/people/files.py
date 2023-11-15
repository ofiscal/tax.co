# The primary purpose of this file is to define the `files` object,
# which describes what and how to retrieve from the raw ENPH data.

if True:
  import python.build.classes as classes
  import python.common.misc as c
  import python.build.classes as cl


edu_key = {
    # PITFALL: Value 9 is not really a value,
    # so in build/people/main.py, it is replaced with np.nan.
    # Otherwise pandas would consider the maximum to be 9 rather than 6.
    1 : "Ninguno",
    2 : "Preescolar",
    3 : "Basica\n Primaria",
    4 : "Basica\n Secundaria",
    5 : "Media",
    6 : "Superior o\n Universitaria",
    9 : "No sabe,\n no informa"
}

race_key = { 1 : "Indigena"
    , 2 : "Gitano-Roma"
    , 3 : "Raizal" # "del archipiélago de San Andrés y Providencia"
    , 4 : "Palenquero" # "de San Basilio o descendiente"
    , 5 : "Negro" # "Negro(a), mulato(a), afrocolombiano(a) o afrodescendiente"
    , 6 : "Ninguno" # "Ninguno de los anteriores (mestizo, blanco, etc.)"
}

demog = [
    ("P6050", 0, "relationship", 0)
  , ("P6020", 0, "female", 0)
  , ("P6040", 0, "age", 0)
  , ("P6080", 0, "race", 0)
  , ("P5170", 0, "pre-k|daycare", 0)
  , ("P6060", 0, "skipped 3 meals", 0)
  , ("P6160", 0, "literate", 0)
  , ("P6170", 0, "student", 0)
  , ("P6210", 0, "edu", 0) # highest level completed
  , ("P6430", 0, "independiente", 0) # 1-3 = asalariado; 4-5 = independiente
                                     # other = no income
]

work = [
  ( "P6240",   0, "last week major activity",             0),
  ( "P6250",   0, "last week worked an hour for pay",     0),
  ( "P6260",   0, "last week had paying job or business", 0),
  ( "P6270",   0, "last week worked an hour without pay", 0),
  ( "P6280",   0, "last month sought work",               0),
  ( "P6310",   0, "last month why did not seek work",     0),
  ( "P6340",   0, "last year sought work",                0),
  ( "P6350",   0, "last week was available to work",      0),
  ( # I don't know what Gabriel wants this for, so I won't interpret it.
    # I'll just thread the raw data through every person-level data set.
    "P6765",   0, "P6765",                                0),
  ( "P6920",   0, "pension, contributing, pre",           0),
  ( "P6920S1", 0, "pension, contribution amount",         0),
  ( "P6940",   0, "pension, contributors, pre",           0),
  ( "P6990",   0, "seguro de riesgos laborales, pre",     0),
]

income_govt = [
  # 5 transfer programs + unemployment payments
    ("P9460S1",   0, "income, month : govt : unemployment", 0)
  , ("P1668S1A1", 0, "income, year : govt : familias en accion", 0)
  , ("P1668S1A4", 0, "income, year : govt : familias en accion, in-kind", 0)
  , ("P1668S3A2", 0, "income, year : govt : familias en su tierra", 0)
  , ("P1668S3A4", 0, "income, year : govt : familias en su tierra, in-kind", 0)
  , ("P1668S4A2", 0, "income, year : govt : jovenes en accion", 0)
  , ("P1668S4A4", 0, "income, year : govt : jovenes en accion, in-kind", 0)
  , ("P1668S2A2", 0, "income, year : govt : programa de adultos mayores", 0)
  , ("P1668S2A4", 0, "income, year : govt : programa de adultos mayores, in-kind", 0)
  , ("P1668S5A2", 0, "income, year : govt : transferencias por victimizacion", 0)
  , ("P1668S5A4", 0, "income, year : govt : transferencias por victimizacion, in-kind", 0)
]

income_labor_non_peso = [
    ("P6760",     0, "income, month : labor : independent, months", 0)
      # Divide P6750 by this to get monthly income.
      # Observed: This is usually 1 or missing, and bounded to [1,12].

  # These are paired with partners in the variable `inclusion_pairs`
  , ("P1653S1A2", 0, "income, month : labor : bonus ?2, included in 6500", 0)
  , ("P1653S2A2", 0, "income, month : labor : bonus, included in 6500", 0)
  , ("P6585S3A2", 0, "income, month : labor : familiar, included in 6500", 0)
  , ("P6585S1A2", 0, "income, month : labor : food, included in 6500", 0)
  , ("P1653S4A2", 0, "income, month : labor : gastos de representacion, included in 6500", 0)
  , ("P6510S2",   0, "income, month : labor : overtime, included in 6500", 0)
  , ("P6585S2A2", 0, "income, month : labor : transport, included in 6500", 0)
  , ("P1653S3A2", 0, "income, month : labor : viaticum, included in 6500", 0) ]

income_labor = [
    ( "P6500",    0, "income, month : labor : formal employment",        0)
  , ( "P7070",    0, "income, month : labor : job 2",                    0)
  , ( "P7472S1",  0, "income, month : labor : as inactive",              0)
  , ( "P7422S1",  0, "income, month : labor : as unemployed",            0)
  , ( # PITFALL: This is net of costs, so that it makes sense
      # to add it to the labor income taxable base.
      "P6750",    0, "income, month : labor : independent",              0)

  # these air paired with partners in the variable `inclusion_pairs`
  , ("P1653S1A1", 0, "income, month : labor : bonus ?2",                 0)
  , ("P1653S2A1", 0, "income, month : labor : bonus",                    0)
  , ("P6585S3A1", 0, "income, month : labor : familiar",                 0)
  , ("P6585S1A1", 0, "income, month : labor : food",                     0)
  , ("P1653S4A1", 0, "income, month : labor : gastos de representacion", 0)
  , ("P6510S1",   0, "income, month : labor : overtime",                 0)
  , ("P6585S2A1", 0, "income, month : labor : transport",                0)
  , ("P1653S3A1", 0, "income, month : labor : viaticum",                 0)

  , ("P6779S1",   0, "income, month : labor : viaticum ?2",              0)

  , ("P550",      0, "income, year : labor : rural",                     0)
  , ("P6630S5A1", 0, "income, year : labor : annual bonus",              0)
    # PITFALL: This needs the apparently-redundant word annual
    # in order not to clobber another variable once yearly variables
    # are converted to monthly ones and accordingly renamed.
  , ("P6630S2A1", 0, "income, year : labor : christmas bonus",           0)
  , ("P6630S1A1", 0, "income, year : labor : prima de servicios",        0)
  , ("P6630S3A1", 0, "income, year : labor : vacation bonus",            0)
  , ("P6630S4A1", 0, "income, year : labor : viaticum ?3",               0)
  , ("P6630S6A1", 0, "income, year : labor : work accident payments",    0)

  , ("P6590S1",   0, "income, month : labor : food, in-kind",            0)
  , ("P6600S1",   0, "income, month : labor : lodging, in-kind",         0)
  , ("P6620S1",   0, "income, month : labor : other, in-kind",           0)
  , ("P6610S1",   0, "income, month : labor : transport, in-kind",       0)
]

income_edu = [
    ("P8610S2", 0, "income, year : edu : beca, in-kind", 0)
  , ("P8610S1", 0, "income, year : edu : beca, cash", 0)
  , ("P8612S2", 0, "income, year : edu : non-beca, in-kind", 0)
  , ("P8612S1", 0, "income, year : edu : non-beca, cash", 0)
]

income_private = [
    ("P7500S3A1", 0, "income, month : private : alimony", 0)
  , ("P7510S3A1", 0, "income, year : private : from private domestic ?firms", 0)
  , ("P7510S4A1", 0, "income, year : private : from private foreign ?firms", 0)
  , ("P7510S1A1", 0, "income, year : private : remittance, domestic", 0)
  , ("P7510S2A1", 0, "income, year : private : remittance, foreign", 0)
]

income_infrequent = [
    ("P7513S9A1",  0, "income, year : infrequent : gambling", 0)
  , ("P7513S10A1", 0, "income, year : infrequent : inheritance", 0)
  , ("P7513S8A1",  0, "income, year : infrequent : jury awards", 0)
  , ("P7513S12A1", 0, "income, year : infrequent : refund, other", 0)
  , ("P7513S11A1", 0, "income, year : infrequent : refund, tax", 0)
]

income_borrowing = [
    ("P7513S6A1", 0, "income, year : borrowing : from bank", 0)
  , ("P7513S7A1", 0, "income, year : borrowing : from other", 0)
  , ("P7513S5A1", 0, "income, year : borrowing : from person", 0)
]

income_capital = [
    ("P7510S10A1", 0, "income, year : investment : dividends", 0)
  , ("P7510S5A1",  0, "income, year : investment : interest", 0)

  , ("P7500S1A1",  0, "income, month : rental : real estate, developed", 0)
  , ("P7500S4A1",  0, "income, month : rental : real estate, undeveloped", 0)
  , ("P7500S5A1",  0, "income, month : rental : vehicle | equipment", 0)

  # The two "sale : stock"  variables record the same information.
  # At least one is always zero.
  # (See python/test/stock_var_non_overlap.py for a proof.)
  # Therefore, income from sale of stock = their maximum = their sum.
  , ("P7510S9A1", 0, "income, year : sale : stock", 0)
  , ("P7513S4A1", 0, "income, year : sale : stock ?2", 0)

  , ("P7513S3A1", 0, "income, year : sale : livestock", 0)
  , ("P7513S1A1", 0, "income, year : sale : real estate", 0)
  , ("P7513S2A1", 0, "income, year : sale : vehicle | equipment", 0)
]

# These form a partition.
income = ( income_govt
         + income_labor
         + income_edu
         + income_private
         + income_infrequent
         + income_borrowing
         + income_capital
         + [ ("P7500S2A1", 0, "income, month : pension : age | illness", 0)
           , ("P7510S6A1", 0, "income, year : cesantia", 0) ]
)

beca_sources_govt = [
    ("P6207M2", 0, "beca from ICETEX", 0)
  , ("P6207M3", 0, "beca from govt, central", 0)
  , ("P6207M4", 0, "beca from govt, peripheral", 0)
  , ("P6207M5", 0, "beca from another public entity", 0)
  , ("P6207M6", 0, "beca from empresa publica ~familiar", 0)
]

beca_sources_private = [
    ("P6207M1", 0, "beca from same school", 0)
  , ("P6207M7", 0, "beca from empresa privada ~familiar", 0)
  , ("P6207M8", 0, "beca from other private", 0)
  , ("P6207M9", 0, "beca from organismo internacional", 0)
  , ("P6207M10", 0, "beca from Universidades y ONGs", 0)
]

inclusion_pairs = [
  # PITFALL: The second of each pair is named for its meaning in the original data.
  # In main.py it is then remapped so that 0=included, 1=omitted.
  #
  # None of the "included in 6500" columns uses an out-of-bounds value
  # like 98 or 99 to indicate an error. (They're all either 1 or 2.)
     ( "income, month : labor : bonus ?2"
     , "income, month : labor : bonus ?2, included in 6500"
  ), ( "income, month : labor : bonus"
     , "income, month : labor : bonus, included in 6500"
  ), ( "income, month : labor : familiar"
     , "income, month : labor : familiar, included in 6500"
  ), ( "income, month : labor : food"
     , "income, month : labor : food, included in 6500"
  ), ( "income, month : labor : gastos de representacion"
     , "income, month : labor : gastos de representacion, included in 6500"
  ), ( "income, month : labor : overtime"
     , "income, month : labor : overtime, included in 6500"
  ), ( "income, month : labor : transport"
     , "income, month : labor : transport, included in 6500"
  ), ( "income, month : labor : viaticum"
     , "income, month : labor : viaticum, included in 6500"
  ) ]

files = [
  # TODO ? This list is inhomogeneous.
  # That might be because I used `0` to represent the empty set,
  # where I should have used `{}`.
  # It doesn't affect execution but it confuses mypy,
  # and it would surely be better to make it homogeneous.
  classes.File( "people"
    , "Caracteristicas_generales_personas.csv"
    ,   c.variables
      + [ ( "ORDEN",
            {cl.StringCellProperty.NotAString},
            "household-member",
            0 ) ]
      + demog
      + work
      + income
      + income_labor_non_peso
      + beca_sources_govt
      + beca_sources_private
      + [ ("P6236", 0, "non-beca sources", 0)
          # PITFALL: Not a number. Instead, a space-separated list of ints.
        , ("P7516", 0, "used savings", 0) ]
          # "1 » Sí 2 » No 3 » No tiene ahorros
    , c.corrections
) ]
