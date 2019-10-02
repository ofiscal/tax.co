-- Anything marked "#ne" is not implemented.
-- Everything else is implemented.
-- Some things are marked "unknowable". However,
-- something might be unknowable even though it bears no such mark.


-- | most income | --

renta liquida laboral =
  ingreso laboral -
  ingresos laborales no constitutivos de renta

renta liquida capital =
  ingreso capital -
  ingreso capital no constitutivo de renta -- #ne, unknowable
  where ingreso capital =
          interest +
          arriendos (literal rent, not profit) +
          regalias -- #ne, unknowable

renta liquida no laboral =
    ingreso no laboral
  - ingreso no laboral no constiotutivo de renta -- #ne, unknowable
  where ingreso no laboral =
          short-term sales +
          non-government becas

cedula general = renta liquida laboral +
                 renta liquida capital +
                 renta liquida no laboral
cedula general gravable = cedula general -
                          min( beneficios
                             , from 25 to 40% of cedula general
                             , 5040 uvt )

renta gravable pension =
    ingreso pension
  - ingreso pension no constitutivo de renta -- #ne
  - renta exenta hasta mil uvt -- #ne

income tax = tarifa 2 ( renta gravable pension +
                        cedula general gravable )

Tarifa 2 =
  min, max income, UVT | rate | total tax paid
  0     | 1090         | 0%   | 0
  1090  | 1700         | 19%  | (Base Gravable - 1090  UVT) x 19%
  1700  | 4100         | 28%  | (Base Gravable - 1700  UVT) x 28% + 116 UVT
  4100  | 8670         | 33%  | (Base Gravable - 4100  UVT) x 33% + 788 UVT
  8670  | 18970        | 35%  | (Base Gravable - 8670  UVT) x 35% + 2296 UVT
  18970 | 31000        | 37%  | (Base Gravable - 18970 UVT) x 37% + 5901 UVT
  31000 | En Adelante  | 39%  | (Base Gravable - 31000 UVT) x 39% + 10352 UVT


-- | other income | --

dividend tax = like 2016,
               but the first 300 UVT are exempt,
               and the rest pay a 15% rate

All other income taxes (specifically:
  ganancia ocasional, gmf, payroll taxes)
  are unchanged.
