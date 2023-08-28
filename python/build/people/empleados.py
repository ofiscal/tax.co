import pandas as pd


def generar_empleados ( df : pd.DataFrame ) -> pd.DataFrame:
  """ Builds these variables:
"ocupado",
"empleado",
"desempleado-abierto",
"desempleado-oculto",
"desempleado",
"in labor force",
  """
  df["ocupado"] = (
    # looks like a definition of ocupado, not empleado
    df.apply(
      ( lambda row:
        1 if (    row["last week major activity"] == 1 # spent it working
               or row["last week worked an hour for pay"] == 1 # at least an hour
               or row["last week had paying job or business"] == 1
                    # got paid for work or a business, even if didn't work.
               or row["last week worked an hour without pay"] == 1 ) # at least an hour
        else 0 ),
      axis=1 ) )

  df["empleado"] = (
    df.apply(
      ( lambda row:
        1 if (    row["last week worked an hour for pay"] == 1 # at least an hour
               or row["last week had paying job or business"] == 1
                    # got paid for work or a business, even if didn't work
               or row["income, labor"] > 2 # PITFALL: 2 COP is basically 0.
                  # Can't test against 0 COP because labor income is fuzzed
                  # to make income quantiles be equally sized.
              )
        else 0 ),
      axis=1 ) )

  df["desempleado-abierto"] = (
    df.apply(
      ( lambda row:
        1 if (           row["last week worked an hour for pay"] == 0
               and       row["last week was available to work"] == 1
                         and ( not row["last week major activity"] in [1,5] ) # Spent it neither working (1) nor incapacitated (5). (Remaining alternatives: study, housework, looking for work, "other".)f
               and (    row["last week major activity"] == 2 # spent it looking for work
                     or row["last month sought work"] == 1 ) )
        else 0 ),
      axis = 1 ) )

  df["desempleado-oculto"] = (
    df.apply(
      ( lambda row:
        1 if (       row["last week worked an hour for pay"] == 0
               and   row["last month sought work"] == 0
               and   row["last year sought work"] == 1
               and   row["last week was available to work"] == 1
               and ( row["last month why did not seek work"] # Legitimately discouraged.
                     in [2,3,4,5,6,7,8] ) )
        else 0 ),
      axis = 1 ) )

  df["desempleado"] = (
    df.apply(
      ( lambda row:
        1 if (    row["desempleado-abierto"] == 1
               or row["desempleado-oculto"]  == 1)
        else 0 ),
      axis = 1 ) )

  df["in labor force"] = ( df["empleado"]    |
                           df["desempleado"] )

  return(df)
