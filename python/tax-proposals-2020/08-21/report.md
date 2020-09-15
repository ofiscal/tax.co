I simulated the parts of the tax proposal that bear on individuals (not corporations), except for the wealth tax, which I can't really say anything about. 

The attached Excel spreadsheet compares the proposal to the current tax scheme (the one issued in 2018).


How to read the spreadsheet
===========================

The first row in that spreadsheet is called "income %ile". It ranges from 1 to 99. (It would ordinarily range from 0 to 99, but the first two percentiles have income equal to zero, so they cannot be distinguished.)

Every other row is an average within that income percentile group. The first one, "income", is the average income in that group. Everything else is the average of some kind of tax.

"Total" is total tax paid. (All amounts are in 2016-2017 pesos.) "Total, prop" is the total they would have paid under the proposed regime. (The word "prop" means "the 2020 proposal" everywhere it appears.) Total tax includes not just the taxes described by the proposal, but also social security contributions, VAT, the predial, and everything else we have data on.

The two "most" columns encompass most income sources. This is "the" income tax, "impuesto a la renta". (I'm saying "the" in quotation marks because ganancias ocasionales, inheritance, and dividends are also income, but they are taxed separately.)

There's only one inheritance tax row, and it corresponds to the proposal. That's because the 2017 regime did not tax inheritance separately; instead, it was part of "ganancia ocasional". In the new regime, ganancia ocasional does not include inheritance. To compare the two regimes, it makes sense to compare "ganancia ocasinoal" to the *sum* of "ganancia ocasinoal, prop" and "inheritance".


Some results that jump out
==========================

Most people are unaffected; they pay the same tax one way or the other. Most peoples' tax bill is almost entirely due to the IVA, and they'll still be paying the same IVA.

Nobody pays the inheritance tax under the proposal. That's because it only kicks in at a really high value. In the old scheme, inheritance was lumped in with "ganancias ocasionales" and the exemption is much lower. So people in our data actually pay some inheritance tax in the old tax regime, and none in the proposed one.

The tax rate on "ganancias ocasionales" in the 2018 tax scheme is 10%. In the proposal it goes as high as 33%. So theoretically, some very rich people will pay more inheritance tax under the new scheme than the old one. But if your intention was not to lower the inheritance tax on anybody, then the threshold at which it begins should be *lower* than the threshold used for ganancias ocasionales. That's because the ganancias ocasionales threshold applies to the sum of inheritance and every other kind of ganancia ocasional (e.g. proceeds from the sale of real estate).

The dividend tax, similarly, collects more revenue from rich people, but less from poor people. The lowest dividend tax rate in the current tax regime is 15%, which kicks in at 300 UVT. In the proposal, at 300 UVT the dividend tax starts at 10%.

In almost all cases the change from the 2018 regime to the proposed one is minor. The only exception is ganancias ocasionalese and inheritances for the top one percent. That looks like this:

income %ile              99
ganancia ocasional       1.17E+05
ganancia ocasional, prop 5.31E+04
inheritance              0.00E+00
                         
Under the 2018 regime, they pay an average of 117000 pesos. Under the proposed one, they pay less than half that, because they are paying no inheritance tax.
