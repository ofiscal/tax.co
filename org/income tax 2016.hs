-- Anything marked "#ne" is not implemented.
-- Everything else is implemented.
-- Some things are marked "unknowable". However,
-- something might be unknowable even though it bears no such mark.


-- | labor + pension income | --

renta liquida laboral =
    ingreso laboral
  - ingresos laborales no constitutivos de renta -- #ne
renta gravable laboral =
    renta liquida laboral
  - min( beneficios
       , from 25% to 40% renta gravable laboral
       , 5040 uvt)

renta gravable pension =
    ingreso pension
  - ingreso pension no constitutivo de renta -- #ne
  - renta exenta hasta mil uvt -- #ne

impuesto tarifa uno aplica a:
  renta gravable (pension + laboral)


-- | capital + nonlabor income | --

renta liquida capital =
  ingreso capital -
  ingreso capital no constitutivo de renta -- #ne, unknowable
  where ingreso capital =
          interest +
          arriendos (literal rent, not profit) +
          regalias (unknowable)

renta gravable de capital =
    renta liquida capital
  - min ( beneficios
        , 10 pct of renta gravable de capital
        , 1000 uvt )

renta liquida no laboral =
    ingreso no laboral
  - ingreso no laboral no constiotutivo de renta -- #ne, unknowable
  where ingreso no laboral =
          short-term sales +
          non-government becas

renta gravable no laboral =
    renta liquida no laboral
  - min( beneficios
       , 10 pct of renta gravable de capital
       , 1000 uvt )

tarifa 2 applies to:
  renta gravable (capital + no laboral)


-- | dividends: done (tarifa 3) | --

-- | ingresos ocasionales | --

renta gravable ocasional, 10%-taxable =
  long-term asset sales +
  inheritance +
  f (donations from private firms)
  where f x = x - min (20% x, 2290 uvt)

renta gravable ocasional, 20%-taxable =
  gambling +
  jury awards


-- | Other thresholds, deductions, exemptions -- #ne

A dependent counts for 10% of the applicable renta liquida.

One only pays income tax if one's various types of incomes exceed various thresholds. See p. 41, orange text, of our Citizen's Guide for details.

ingresos no constitutivo de renta =
    ss contributions
  + gmf / 2
  + things we don't have information about
