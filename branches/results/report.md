The covid crisis has left many Colombians with little or no work. Those who can do so are using their savings to survive. It is reasonable to wonder: How long does it take a Colombian household to save for a month?

The Encuesta Nacional de Preupuestos de Hogares is a survey of 87201 Colombian households (291590 people) that was conducted over 2016 and 2017. It is a rich, wonderful data set, with detailed information on sources of income and expenses (and many other things). The purchase data includes everything a household purchased over a month.

The math we need to do is easy. If a household saves zero or fewer pesos per month, then they can never save enough money for a month of expenses. Otherwise, the number of months a household needs in order to save for a month is "spending / saving". For instance, a household that spends 1 million pesos and saves 200,000 in a month would take 5 months to save for one month.

The ENPH includes data on whether someone drew down their savings in the month they were interviewed. Presumably, a month like that is not a normal month for a household. Those households are therefore not part of this analysis.[footnote 1]

Here are the results.

              0.1   0.2   0.3   0.4   0.5    0.6  0.7  0.8  0.9  1.0
full sample  0.09  0.21  0.42  0.86  2.01  12.30  inf  inf  inf  inf

Each cell is what's called a "decile". It's easiest to define what those are through examples. The first cell, in the column labeled 0.1, is 0.09. This means that 10 percent of households are able to save up for a month in 0.09 months -- about 3 days. These households make a lot more money than they spend. If we keep reading along that row, we find that 20% of Colombian households are able to save for a month of expenses in 0.21 months -- about six days. 50% are able to save for a month in 1.82 months. 60% are able to save for a month in 10.86 months.

Then the numbers jump to infinity! Somewhere between the 6th and 7th decile, people stop being able to save at all. We can zoom in with more detail, looking at "percentiles" instead of "deciles":

                0.60   0.61   0.62  0.63  0.64  1.00
full sample    12.30  21.09  85.61   inf   inf   inf

This shows that 62 percent of Colombian households are able to save up for a month's worth of expenses in 62 months or less. Everybody else -- 38% of the population! -- is spending more than they save[footnote 2].

Those are the quantiles across the entire population. It's interesting to see what happens to particular subgroups too. The table below does that. The second row looks at households with 3 or more members. The third row is households in which the head of household is female. (These are probably mostly single mothers.) The last two rows describe households with a child (someone under 18) and households with someone elderly (over 65).

              0.1   0.2   0.3   0.4   0.5    0.6  0.7  0.8  0.9  1.0
full sample  0.09  0.21  0.42  0.86  2.01  12.30  inf  inf  inf  inf
3 or more    0.12  0.27  0.56  1.16  3.04    inf  inf  inf  inf  inf
female head  0.11  0.28  0.60  1.21  3.07    inf  inf  inf  inf  inf
has child    0.12  0.25  0.52  1.09  2.87    inf  inf  inf  inf  inf
has elderly  0.07  0.19  0.40  0.80  1.76  13.91  inf  inf  inf  inf

In all subgroups the number of people unable to save any money at all is around 40%. If we zoom in on the 5th and 6th deciles we can be more precise about that:

              0.57   0.58   0.59   0.60   0.61   0.62  0.63  1.00
full sample   5.09   6.34   8.57  12.30  21.09  85.61   inf   inf
3 or more    13.33  21.19  62.33    inf    inf    inf   inf   inf
female head  16.76  36.54    inf    inf    inf    inf   inf   inf
has child    11.32  17.48  39.35    inf    inf    inf   inf   inf
has elderly   4.77   6.23   9.11  13.91  30.23    inf   inf   inf

In each case, at least 37% of the subsample is unable to save any money at all.

This analysis assumes that the spending reported by a household during the survey is representative of an average month for that household. If you imagine a household that earns a lot of money for a few months of the year, and makes no money the rest of the year, then if they were surveyed during a month of high earning they would appear to save quickly, and if they were surveyed in another month they would appear to be unable to save.

Similarly, we need to assume that the expenses the household reports for that month are representative.

Both of those assumptions are unlikely to hold perfectly, so these numbers are not the final story. That said, it's unclear whether the truth is better or worse. What's clear, though, is that a huge fraction of Colombians find it difficult or impossible to save money. Without assistance or a return to work they are in serious danger.

The code that generated this report is public. You can find it, and run it yourself if you like, at 
https://github.com/ofiscal/tax.co/blob/time-to-save-for-a-month/python/months_to_save_for_a_month.py


# Footnotes

[1] The ENPH also says whether a household recently moved. Suspecting that moving might temporarily increase a house's expenses, I tried excluding those households from the analysis. It turns out to make no meaningful difference -- mostly because very few households (fewer than 5%) moved.

[2] Actually, given this table, all we can say for sure is it's somewhere between 37% and 38% of the population. Just as we zoomed into the decile from 60% to 70%, we would have to zoom in on the percentile from 62% to 63% to be more precise.
