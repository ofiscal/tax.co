
## Household spending and taxes / by income
households["income-decile"] = pd.qcut(people["income"], 10, labels = False)
