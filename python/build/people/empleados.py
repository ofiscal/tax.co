import pandas as pd


def generar_empleados ( df : pd.DataFrame ) :
  df["ocupado"] = (
    # looks like a definition of ocupado, not empleado
    df.apply(
      ( lambda row:
        1 if (    row["P6240"] == 1 # Worked most of last week.
               or row["P6250"] == 1 # Got paid for at least an hour last week.
               or row["P6260"] == 1 # Last week got paid for work or a business,
                                  # even if didn't work.
               or row["P6270"] == 1 ) # Worked at least an hour without pay last week.
        else 0 ),
      axis=1 ) )

  df["empleado"] = (
    df.apply(
      ( lambda row:
        1 if (    row["P6250"] == 1 # Got paid for at least an hour last week.
               or row["P6260"] == 1 # Last week got paid for work or a business, even if didn't work.
               or row["income, labor"] > 0
              )
        else 0 ),
      axis=1 ) )

  df["desempleado-abierto"] = (
    df.apply(
      ( lambda row:
        1 if (           row["P6250"] == 2 # was *not* paid for at least an hour
               and       row["P6350"] == 1 # was able to work. Students answer no to this.
               and ( not row["P6240"] in [1,5] ) # Spent most of last week neither neither working (1) nor incapacitated (5). (Remaining alternatives are study, housework, and looking for work, and "other".)
                     # What about n/a?
               and (    row["P6240"] == 2     # Spent most of last week looking for work.
                     or row["P6280"] == 1 ) ) # looked for work in the last 4 weeks
        else 0 ),
      axis = 1 ) )

  df["desempleado-oculto"] = (
    df.apply(
      ( lambda row:
        1 if (       row["P6250"] == 2 # was *not* paid for at least an hour
               and   row["P6280"] == 2 # Did *not* look for work in the last 4 weeks.
               and   row["P6340"] == 1 # Looked for work in the last 12 months.
               and   row["P6350"] == 1 # Was able to work last week.
               and ( row["P6310"] # Legitimately discouraged.
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

  return(df)
