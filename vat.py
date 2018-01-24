# The value-added tax.

import numpy as np
import pandas as pd
import util as util

world = pd.DataFrame.from_csv("data/world.csv")
people = pd.DataFrame.from_csv("data/people.csv")

world["tax"] = world["price"] * world["taxRate"] # do once, not per person

if not (world.index == people.index).all():
    util.printInRed(
        "Error: The indices (lists of goods) for world and people differ." )

else:
    whatWhoPaid = people.apply( lambda row:
                                np.dot( row, world["tax"] ) )
    whatWhoPaid.name = "totalVatPaid"
    people = people.append(whatWhoPaid)
