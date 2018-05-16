# to be used in conjunction with for-report.py

%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt

plt.hist(
  purchases["frequency"].dropna(),
  normed=True, cumulative=True, label='CDF',
  histtype='step', alpha=0.8, color='k')
plt.show()
plt.savefig("test.png")
