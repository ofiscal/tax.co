I discovered the inconsistencies in the process of translating the law to Python code.


# The dividend tax schedule

Let's start with the part of the law where I found no inconsistencies, which is the dividend tax. Here's what that looks like in the proposal:

![dividends](pics/dividends/dividends.png)

What that says is that if someone's dividend income is less than 300 uvts, they pay no dividend tax. If it's not less than 300 but it's less than 600 uvts, then they pay 10% tax on the portion of their dividend income in excess of 300 uvts. If their dividend income is not less than 600 uvt but it's less than 1000 uvt, they pay 18% on the portion above 600, and they also pay 30 uvt for the first 600. Etc.

There are a couple important patterns in it.

## Pattern 1: Subtract the top of the previous bracket from the income subject to the current bracket.

Notice how the 300 in the "hasta" column of the first row is subtracted from income in the formula ("impuesto") column of the second row:

![dividend_thresholds_correspond](pics/dividends/dividend-tax-thresholds-correspond.png).

Similarly, the 600 from the second row appears in the formula for the third row, etc. This pattern is common to tax schedules. Since each peso earned should be taxed by exactly one rate (maybe zero), the pesos that were taxed at earlier rates are subtracted from income when the next rate is applied.

## Pattern 2: Add the maximum payable tax leviable by the previous bracket to the tax dictated by the current bracket.

If you plug in the maximum amount of income that could be taxed in any row, the result is the amount that is added to someone's taxes in the next row. For instance:

![didivend_schedule_deriving_the_summand_from_the_previous_line](pics/dividends/dividends-plug-prev-max-into-prev-formula.png)

If you plug 600 into the second row, you get 30, and 30 is the amount added in the third row. If you plug 1000 into the third row, you get 78, which is the amount added in the fourth row. Etc. (In the first row, if you plug in 300, you get 0, which is why nothing is added in the formula for the second row.)

The dividend tax proposed follows these rules consistently. The others do not.


# The inheritance tax

There are two problems with the proposed inheritance tax schedule. The first is that the biggest inheritances are not in fact being taxed at a 33% rate, as suggested by the "Tarifa Marginal" column, but rather just 25%:

![inheritance tax rate mismatch](pics/inheritance/rate-mismatch.png)

The second is that the `112337` from the first row should be subtracted from `x` in the second row:

![inheritance tax non-marginal mass point](pics/inheritance/non-marginal.png)

Without this, we have the strange result that if someone inherits `112336` UVTs, they pay no inheritance tax, but if they inherit `112338` UVTs, they lose 10% of their entire inheritance to taxes.


# The wealth tax (in progress)

The weatlh tax schedule gives a uniform, intuitive set of marginal rates, starting at 1% and progressing up to 4%. However, the formulas dictating total tax owed as a function of those rates appear to be incorrect.

Their first inconsistency is in Pattern 1. It is only followed about half the time. The circles in the picture below indicate where it *is* followed:

![wealth tax bounds mismatch](pics/wealth/bounds-mismatch.png)

The most pronounced effect of this pattern not being followed is in the highest wealth bracket:

![wealth tax negative](pics/wealth/negative.png)

If you plug 3.000.000 into the formula proposed, the resulting tax is actually negative:
```
(3000000 - 14042183 )*0.04  + 74990 = -366697.32
```

In fact, for any level of wealth below 12167433 UVTs, the tax levied by the formula. If your wealth was exactly 12167433 UVT, you would owe 0 in taxes. If your wealth was (12167433 + 100) UVT greater than that number, you would owe 4 UVT in taxes. Meanwhile someone whose wealth was much lower than yours, 2808436 UVTs, would owe 74990 in taxes.

It looks like Congress intended to implement the following marginal rate schedule:

| From    | To      | Rate |
| --      | --      | --   |
| 0       | 84253   | 0%   |
| 84253   | 140422  | 1%   |
| 140422  | 280844  | 1.5% |
| 280844  | 702109  | 2%   |
| 702109  | 1404218 | 2.5% |
| 1404218 | 2106327 | 3%   |
| 2106327 | 2808437 | 3.5% |
| 2808437 | infinity| 4%   |

If so, then the table in the proposal should look like this:

| Límite inferior         | Límite superior | Tarifa                                           |
| --                      | --              | --                                               |
| Mayor o Igual a   84253 | Menor a  140422 | Patrimonio menos 84253 UVT * 1%                  |
| Mayor o Igual a  140422 |          280844 | Patrimonio menos  140422 UVT * 1.5% + 562   UVTs |
| Mayor o Igual a  280844 |          702109 | Patrimonio menos  280844 UVT * 2%   + 2668  UVTs |
| Mayor o Igual a  702109 |         1404218 | Patrimonio menos  702109 UVT * 2.5% + 11093 UVTs |
| Mayor o Igual a 1404218 |         2106327 | Patrimonio menos 1404218 UVT * 3%   + 28646 UVTs |
| Mayor o Igual a 2106327 |         2808437 | Patrimonio menos 2106327 UVT * 3.5% + 49709 UVTs |
| Mayor o Igual a 2808437 |        ifninito | Patrimonio menos 2808437 UVT * 4%   + 74283 UVTs |
