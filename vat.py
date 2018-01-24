# The value-added tax.
import numpy as np
import pandas as pd

# read
world = pd.DataFrame.from_csv("data/world.csv")
people = pd.DataFrame.from_csv("data/people.csv")

# do this once, not per person
world["tax"] = world["price"] * world["taxRate"]

whatWhoPaid = people.apply( lambda row:
                            np.dot( row, world["tax"] ) )
whatWhoPaid.name = "totalVatPaid"
people = people.append(whatWhoPaid)
