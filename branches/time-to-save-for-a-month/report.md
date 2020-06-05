The covid crisis has left many Colombians with little or no work. Those who can do so are using their savings to survive. It is reasonable to wonder: How long does it take a Colombian household to save for a month?

The Encuesta Nacional de Preupuestos de Hogares is a survey of 87201 Colombian households (291590 people) that was conducted over 2016 and 2017. It is rich data, with detailed information on, among many other things, a household's income and its purchases.

The math to do is easy. If a household saves zero or fewer pesos per month, then they can never save enough money for a month of expenses. Otherwise, the number of months a household needs in order to save for a month is "spending / saving". For instance, a household that spends 1 million pesos and saves 200,000 in a month would take 5 months to save for one month.

The ENPH includes data on whether someone drew down their savings in the month they were interviewed. Presumably, a month like that is not a normal month for a household. Those households are therefore excluded from this analysis.[footnote 1]

Here are the results.

```
              0.1   0.2   0.3    0.4  0.5  0.6  0.7  0.8  0.9  1.0
full sample  0.66  1.39  3.48  73.93  inf  inf  inf  inf  inf  inf
```

Each cell is what's called a "decile". It's easiest to define what those are through examples. The first cell, in the column labeled 0.1, is 0.66. This means that 10 percent of households are able to save up for a month in 0.66 months -- about 20 days. These households make a lot more money than they spend -- although that does not mean they're rich[footnote 2]. If we keep reading along that row, we find that 20% of Colombian households are able to save for a month of expenses in 1.39 months or less. 30% can save for a month in 3.48 months or less. 40% can save for a month in less than 73 months (about six years).

Then the numbers jump to infinity. In the 5th decile, people are unable to save at all -- they spend more than they save.

Those are the quantiles across the entire population. It's worth asking what happens to particular subgroups, too. The table below does that. The second row looks at households with 3 or more members. The third row is households in which the head of household is female. (These are probably mostly single mothers.) The the last two rows describe households with a child (under 18) and households with someone elderly (over 65).

```
              0.1   0.2   0.3    0.4  0.5  0.6  0.7  0.8  0.9  1.0
full sample  0.66  1.39  3.48  73.93  inf  inf  inf  inf  inf  inf
3 or more    0.70  1.47  3.70  80.82  inf  inf  inf  inf  inf  inf
female head  0.78  1.81  5.97    inf  inf  inf  inf  inf  inf  inf
has child    0.75  1.53  3.97    inf  inf  inf  inf  inf  inf  inf
has elderly  0.60  1.31  3.43  55.97  inf  inf  inf  inf  inf  inf
```

In all subgroups the number of people unable to save any money at all is around 40%. If we zoom in on the 3rd and 4th deciles we can be more precise about that:

```
             0.32   0.33   0.34   0.35   0.36   0.37   0.38   0.39   0.40  0.41  0.42  0.43
full sample  4.50   5.15   6.05   7.25   8.97  11.76  16.80  27.09  73.93   inf   inf   inf
3 or more    4.77   5.42   6.54   7.66   9.67  12.52  17.32  27.84  80.82   inf   inf   inf
female head  9.44  13.53  20.26  46.54    inf    inf    inf    inf    inf   inf   inf   inf
has child    5.11   6.06   7.22   8.61  11.43  16.00  26.10  70.36    inf   inf   inf   inf
has elderly  4.33   4.88   5.63   6.61   8.03   9.95  13.53  21.08  55.97   inf   inf   inf
```

In each subsample, at least 59% of households are unable to save any money at all. Households with at least one child, and especially households in which the head of household is female, are substantially less able to save.

This analysis assumes that the spending reported by a household during the survey is representative of an average month for that household. If a household earns a lot of money for a few months of the year, and makes no money the rest of the year, and if that household surveyed during a month of high earning, then that household would appear to save quickly. Conversely, if that household was surveyed in another month, they would appear to be unable to save.

Similarly, the analysis assumes that the expenses the household reports for that month are representative.

Both of those assumptions are unlikely to hold perfectly, so these numbers are not the final story. That said, it's not clear whether the truth is better or worse. What is clear, though, is that an enormous fraction of Colombians find it difficult or impossible to save money. Without assistance or a return to work they are in serious danger.

The code that generated this report is public, available at
https://github.com/ofiscal/tax.co/blob/time-to-save-for-a-month/python/months_to_save_for_a_month.py


# Footnotes

[1] The ENPH also says whether a household recently moved. Suspecting that moving might temporarily increase a house's expenses, I tried excluding those households from the analysis. It turns out to make no meaningful difference -- mostly because very few households (fewer than 5%) moved.

[2] 45% of the top decile of savers made less than 1500000/month. (The data are from 2016-2017; the peso was worth a little more then.) The survey is for all of Colombia, across which the cost of living varies greatly, cities and especially Bogotá being the most expensive.

By definition, saving = income - spending. It does not take into account gifts or subsistence production. A family that receives a lot of charity might appear to consume much less than it does, and a family on a farm could theoretically spend no money at all.

[3] This table indicates that somewhere between 42% and 43% of the population spends less than they earn (and therefore somewhere between 57% and 58% of the population spends more than they earn). Just as we zoomed into the 3rd and 4th deciles, we would have to zoom in on the percentile from 42% to 43% to be more precise.
