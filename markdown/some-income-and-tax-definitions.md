The terms in the denominator of Equation 1 of our paper on the microsimulation
do not correspond very tightly with the income tax calculations in the sim.
That calculation consists of these components:

    income_tax_components =
      [ "tax, income, most", # includes all labor and some nonlabor income
        "tax, income, dividend",
        "tax, income, ganancia ocasional",
        "tax, income, gmf", ]

Meanwhile the denominator of equation 1 is

    net labor income
    + capital income
    + dividends
    + payroll contributions
    + pension income

Our definition of "income, labor" is, roughly, a sum of these values,
after appropriate massaging of each one.
Note that some of these are the peso values of in-kind income.

    income_labor = [
        ("P6500", 0, "income, month : labor : formal employment", 0)
      , ("P7070", 0, "income, month : labor : job 2", 0)
      , ("P7472S1", 0, "income, month : labor : as inactive", 0)
      , ("P7422S1", 0, "income, month : labor : as unemployed", 0)
      , ("P6750", 0, "income, month : labor : independent", 0)

      # these air paired with partners in the variable `inclusion_pairs`
      , ("P1653S1A1", 0, "income, month : labor : bonus ?2", 0)
      , ("P1653S2A1", 0, "income, month : labor : bonus", 0)
      , ("P6585S3A1", 0, "income, month : labor : familiar", 0)
      , ("P6585S1A1", 0, "income, month : labor : food", 0)
      , ("P1653S4A1", 0, "income, month : labor : gastos de representacion", 0)
      , ("P6510S1", 0, "income, month : labor : overtime", 0)
      , ("P6585S2A1", 0, "income, month : labor : transport", 0)
      , ("P1653S3A1", 0, "income, month : labor : viaticum", 0)

      , ("P6779S1", 0, "income, month : labor : viaticum ?2", 0)

      , ("P550", 0, "income, year : labor : rural", 0)
      , ("P6630S5A1", 0, "income, year : labor : annual bonus", 0)
        # PITFALL: This needs the apparently-redundant word annual
        # in order not to clobber another variable once yearly variables
        # are converted to monthly ones and accordingly renamed.
      , ("P6630S2A1", 0, "income, year : labor : christmas bonus", 0)
      , ("P6630S1A1", 0, "income, year : labor : prima de servicios", 0)
      , ("P6630S3A1", 0, "income, year : labor : vacation bonus", 0)
      , ("P6630S4A1", 0, "income, year : labor : viaticum ?3", 0)
      , ("P6630S6A1", 0, "income, year : labor : work accident payments", 0)

      , ("P6590S1", 0, "income, month : labor : food, in-kind", 0)
      , ("P6600S1", 0, "income, month : labor : lodging, in-kind", 0)
      , ("P6620S1", 0, "income, month : labor : other, in-kind", 0)
      , ("P6610S1", 0, "income, month : labor : transport, in-kind", 0)
    ]

Here's the definition of capital income:

    ppl["income, capital"] = (
      ppl [ [ "income, dividend",
              "income, rental + interest",
              "income, sale not real estate",
              "income, sale, real estate", ] ]
      . sum ( axis = 1 ) )

That's a quantity we define and then never use to compute anything else
(except its average in various subpopulations).

Dividend income is a single variable reported in the ENPH:
("P7510S10A1", 0, "income, year : investment : dividends", 0),
later renamed to "income, dividend".
That's what we use to compute the dividend income tax.

`payroll` is *extremely* complicated, but the idea is that,
based on someone's monthly income and whether they are an "independiente",
we impute all of these:

  "cesantias + primas"
  "tax, ss, cajas de compensacion"
  "tax, ss, parafiscales"
  "tax, ss, pension"
  "tax, ss, pension, employer"
  "tax, ss, salud"
  "tax, ss, salud, employer"
  "tax, ss, solidaridad"

and call the result "tax, ss".
("independiente" comes from a single variable in the ENPH, P6430,
for which 1-3 mean "asalariado" and 4-5 mean independiente.)

Pension income, like dividend income, is a single variable in the ENPH:
"P7500S2A1" : "income, month : pension : age | illness",
later renamed to "income, pension".
