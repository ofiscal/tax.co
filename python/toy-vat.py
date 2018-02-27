# The value-added tax.

import numpy as np
import pandas as pd
import util as util

taxes = pd.DataFrame.from_csv("data/toy/taxes.csv")
spending = pd.DataFrame.from_csv("data/toy/spending.csv")

taxes["tax"] = taxes["price"] * taxes["taxRate"] # do once, not per person

if not (taxes.index == spending.index).all():
    util.printInRed(
        "Error: The indices (lists of goods) for tax rates and spending differ." )
else:
    whatWhoPaid = people.apply( lambda row:
                                np.dot( row, taxes["tax"] ) )
    whatWhoPaid.name = "totalVatPaid"
    spending = spending.append(whatWhoPaid)
