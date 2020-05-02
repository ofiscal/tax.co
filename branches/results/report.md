The covid crisis has left many Colombians with little or no work. Those who can do so are using their savings to survive. It is reasonable to wonder: How long does it take a Colombian household to save for a month?

The Encuesta Nacional de Preupuestos de Hogares is a survey of 87201 Colombian households (291590 people) that was conducted over 2016 and 2017. It is rich data, with detailed information on, among many other things, a household's income and its purchases.

The math to do is easy. If a household saves zero or fewer pesos per month, then they can never save enough money for a month of expenses. Otherwise, the number of months a household needs in order to save for a month is "spending / saving". For instance, a household that spends 1 million pesos and saves 200,000 in a month would take 5 months to save for one month.

The ENPH includes data on whether someone drew down their savings in the month they were interviewed. Presumably, a month like that is not a normal month for a household. Those households are therefore excluded from this analysis.[footnote 1]

Here are the results.

              0.1   0.2   0.3   0.4   0.5    0.6  0.7  0.8  0.9  1.0
full sample  0.09  0.21  0.43  0.88  2.07  14.52  inf  inf  inf  inf

Each cell is what's called a "decile". It's easiest to define what those are through examples. The first cell, in the column labeled 0.1, is 0.09. This means that 10 percent of households are able to save up for a month in 0.09 months -- about 3 days. These households make a lot more money than they spend. If we keep reading along that row, we find that 20% of Colombian households are able to save for a month of expenses in 0.21 months -- about six days. 50% are able to save for a month in 2.07 months. 60% are able to save for a month in 14.52 months.

Then the numbers jump to infinity! Somewhere between the 6th and 7th decile, people stop being able to save at all. We can zoom in with more detail, looking at "percentiles" instead of "deciles":

              0.59   0.60   0.61    0.62  0.63  0.64
full sample   9.70  14.52  28.95  267.27   inf   inf

This shows that 62 percent of Colombian households are able to save up for a month's worth of expenses in 267.27 months or less. Everybody else is spending more than they earn[footnote 2].

Those are the quantiles across the entire population. It's interesting to see what happens to particular subgroups, too. The table below does that. The second row looks at households with 3 or more members. The third row is households in which the head of household is female. (These are probably mostly single mothers.) The last two rows describe households with a child (someone under 18) and households with someone elderly (over 65).

              0.1   0.2   0.3   0.4   0.5    0.6  0.7  0.8  0.9  1.0
full sample  0.09  0.21  0.43  0.88  2.07  14.52  inf  inf  inf  inf
3 or more    0.13  0.27  0.58  1.18  3.20    inf  inf  inf  inf  inf
female head  0.11  0.29  0.62  1.25  3.27    inf  inf  inf  inf  inf
has child    0.12  0.25  0.53  1.11  3.01    inf  inf  inf  inf  inf
has elderly  0.07  0.19  0.40  0.81  1.83  17.50  inf  inf  inf  inf

In all subgroups the number of people unable to save any money at all is around 40%. If we zoom in on the 5th and 6th deciles we can be more precise about that:

              0.57   0.58    0.59   0.60   0.61    0.62  0.63  0.64
full sample   5.42   7.00    9.70  14.52  28.95  267.27   inf   inf
3 or more    15.28  28.44  127.51    inf    inf     inf   inf   inf
female head  21.99  89.89     inf    inf    inf     inf   inf   inf
has child    13.45  22.18   84.19    inf    inf     inf   inf   inf
has elderly   5.10   6.80   10.26  17.50  48.28     inf   inf   inf

In each case, at least 37% of the subsample is unable to save any money at all.

This analysis assumes that the spending reported by a household during the survey is representative of an average month for that household. If a household that earns a lot of money for a few months of the year, and makes no money the rest of the year, was surveyed during a month of high earning, then that household would appear to save quickly. Conversely, if that household was surveyed in another month, they would appear to be unable to save.

Similarly, we need to assume that the expenses the household reports for that month are representative.

Both of those assumptions are unlikely to hold perfectly, so these numbers are not the final story. That said, it's unclear whether the truth is better or worse. What's clear, though, is that a huge fraction of Colombians find it difficult or impossible to save money. Without assistance or a return to work they are in serious danger.

The code that generated this report will soon be public.[3]


# Footnotes

[1] The ENPH also says whether a household recently moved. Suspecting that moving might temporarily increase a house's expenses, I tried excluding those households from the analysis. It turns out to make no meaningful difference -- mostly because very few households (fewer than 5%) moved.

[2] This table indicates that somewhere between 37% and 38% of the population is spending more than they earn. Just as we zoomed into the decile from 60% to 70%, we would have to zoom in on the percentile from 62% to 63% to be more precise.

[3] Early versions of the code are already public, available here:
https://github.com/ofiscal/tax.co/blob/time-to-save-for-a-month/python/months_to_save_for_a_month.py
Github is temporarily not allowing me to upload changes, but once it does, the latest version will be there.
