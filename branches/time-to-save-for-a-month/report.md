The covid crisis has left many Colombians with little or no work. Those who can do so are using their savings to survive. It is reasonable to wonder: How long does it take a Colombian household to save for a month?

The Encuesta Nacional de Preupuestos de Hogares is a survey of 87201 Colombian households (291590 people) that was conducted over 2016 and 2017. It is rich data, with detailed information on, among many other things, a household's income and expenses.

The math to do is easy. If a household saves zero or fewer pesos per month, then they can never save enough money for a month of expenses. Otherwise, the number of months a household needs in order to save for a month is "spending / saving". For instance, if a household spends 1 million pesos and saves 200,000 in a month, then it would take 5 months to save for one month.

The question of which income and spending to take into account is not as easy as one might imagine. For instance, if a family bought a car when they were surveyed, their spending in the survey would (unless they buy cars frequently) be higher than it usually is. Similarly, if they sold a car, their income would appear higher than its average.

Fortunately, the ENPH provides aggregate income and expense data that allows us to handle such problems conservatively[footnote 0].

Here are the results.

```
               0.1   0.2   0.3   0.4   0.5  0.6  0.7  0.8  0.9  1.0
full sample   0.78  1.34  2.25  4.29 15.97  inf  inf  inf  inf  inf
```

Each cell is what's called a "decile". It's easiest to define what those are through examples. The first cell, in the column labeled 0.1, is 0.78. This means that 10 percent of households are able to save up for a month in 0.78 months (about 23.4 days). These households make a lot more money than they spend -- although that does not mean they're rich[footnote 2]. If we keep reading along that row, we find that 20% of Colombian households are able to save for a month of expenses in 1.34 months or less; 30% can save for a month in 2.25 months or less; 40% in 4.29 months or less; and 50% in 16 months or less.

Then the numbers jump to infinity. Somewhere in the 5th decile, people become unable to save at all -- they spend more than they save.

Those quantiles are across the entire population. It's worth asking what happens to particular subgroups, too. The table below does that. The second row looks at households with 3 or more members. The third row is households in which the head of household is female. The the last three rows describe households with a child (under 18), households in which every member is elderly (over 65), and households in which someone but not everyone is elderly.

```
               0.1   0.2   0.3   0.4     0.5    0.6  0.7  0.8  0.9  1.0
full sample   0.78  1.34  2.25  4.29   15.97    inf  inf  inf  inf  inf
3 or more     0.83  1.41  2.36  4.46   16.54    inf  inf  inf  inf  inf
female head   0.83  1.48  2.69  5.81  101.78    inf  inf  inf  inf  inf
has child     0.95  1.69  3.03  7.03     inf    inf  inf  inf  inf  inf
all elderly   0.55  1.02  1.64  3.04    9.66    inf  inf  inf  inf  inf
some elderly  0.63  1.02  1.51  2.44    4.53  22.44  inf  inf  inf  inf
```

In every subgroup, the number of people unable to save any money at all is around 50%. If we zoom in on the quantiles where that transition occurs, we can be more precise:

```
               0.48    0.49    0.50   0.51   0.52   0.53     0.54  0.55  0.56   0.57   0.58   0.59   0.60   0.61   0.62     0.63  0.64  0.65
full sample   10.66   12.62   15.97  20.72  31.16  63.54   721.54   inf   inf    inf    inf    inf    inf    inf    inf      inf   inf   inf
3 or more     11.13   13.33   16.54  21.37  31.56  60.91   649.70   inf   inf    inf    inf    inf    inf    inf    inf      inf   inf   inf
female head   25.48   40.03  101.78    inf    inf    inf      inf   inf   inf    inf    inf    inf    inf    inf    inf      inf   inf   inf
has child     46.59  132.15     inf    inf    inf    inf      inf   inf   inf    inf    inf    inf    inf    inf    inf      inf   inf   inf
all elderly    7.12    8.38    9.66  13.21  22.66  77.41  1069.05   inf   inf    inf    inf    inf    inf    inf    inf      inf   inf   inf
some elderly   3.89    4.17    4.53   4.86   5.22   5.57     6.22  7.19  8.05  10.28  12.47  16.27  22.44  29.95  57.29  1318.02   inf   inf
```

In almost every subsample, fewer than 55% of households are able to save any money at all. For households with at least one child, and households in which the head of household is female, it is substantially more difficult to save.

Households in which someone but not everyone is elderly are an outlier. These households appear to save much more -- whereas only 54% of Colombian households as a whole are able to save, 63% of mixed-elderly households can. I would like to imagine that elder members impart important financial advice to younger earners -- but, of course, other explanations are possible.

What the data make clear is that an enormous fraction of Colombian households are unable to save at all. Without assistance or a return to work, they are in serious danger.

The code that generated this report is public, available at
https://github.com/ofiscal/tax.co/tree/master/python/report/time_to_save_for_a_month


# Footnotes

[0] "Ingreso Corriente Monetario Disponible" represents a household's usual cash income after automatic deductions. "Usual" means it excludes income from rare events like the sale of a vehicle. "Cash" stands as opposed to in-kind income -- for instance, if one's employer provides food, that counts as income, but it is not cash income. Automatic deductions include things like pension and social security contributions.

Similarly, "Gasto Corriente Monetario" is a household's usual cash spending. ("Gasto Monetario" might seem redudnant -- how does one spend without spending money -- but it's not, because the ENPH includes barter transactions.)

Those two variables are constructed by DANE as elaborate sums from the raw data; they are not directly reported by survey respondents. As a robustness check, I used "naive" total income and spending variables, which do not attempt to ignore unusual flows of money. Using those variables gives a much grimmer picture of savings in Colombia. In particular, the fraction of people unable to save at all rises from about 50% to about 60%.

The ENPH sample is really big. There is no obvious reason to expect unusual expenses to systematically outweigh unusual income. An estimate of savings from the "naive" income and expenditure variables should therefore be roughly in line with an estimate that ignores unusual flows.

I expect the truth lies somewhere between them.

[2] 15% of the top decile of savers made less than 1600000/month. If that seems strange, bear a few things in mind:

The data are from 2016-2017, a period in which the peso was worth a little more.

The survey is for all of Colombia, across which the cost of living varies greatly. Cities, especially Bogotá, are the most expensive places to live.

By definition, saving = income - spending. It does not take into account gifts or subsistence production. Considering only its expenses, a family that receives a lot of charity might appear to consume much less than it does. And a family on a farm could theoretically spend no money at all.
