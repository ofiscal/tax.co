def maybeFill(groupVar, val):
  if groupVar == "income-percentile":
    return val.zfill(2)
  else: return val
