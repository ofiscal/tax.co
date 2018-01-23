# The value-added tax.

import numpy as np

goods = np.array( ["banana","guitar"] )
# vectors: purchases, prices, taxes

purchases = np.array( [1, 2] )
prices = np.array( [1, 100] )
taxes = np.array( [.1, .2] )

revenue = np.dot( purchases * prices, taxes )
