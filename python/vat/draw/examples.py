import python.vat.draw.util as draw
import pandas as pd

%matplotlib inline
  # enable the previous line if calling from Jupyter
import matplotlib
# matplotlib.use('Agg')
  # enable the previous line if calling from the (non-gui) shell
import matplotlib.pyplot as plt


the_data = pd.DataFrame([1,2,7,2,7],columns=["x"])
draw.cdf( the_data["x"] )
plt.title("The empirical CDF of the observed series 1,2,7,2,7")
plt.xlabel("Outcome")
plt.ylabel("Probability")
if True: # alternatives
  # plt.show()
  plt.savefig("test.png")
