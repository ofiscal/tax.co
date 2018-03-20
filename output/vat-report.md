# What is the VAT

The VAT is a kind of tax, one levied on purchases of goods and services. The government receives revenue from many other types -- the individual and corporate income taxes, real estate taxes, taxes on alcohol, tobacco, and gas, tariffs ... However the VAT is its single biggest revenue source. The VAT goes entirely to the federal government, which derives 1/3 of revenues from it. Federal tax revenue is 80% of total tax revenue in Colombia.


## What fraction of the price is the VAT

The default level of the VAT is 19%. There are numerous exemptions, however; the tax code singles out 310 categories of goods and services, some quite broad, for special VAT treatment. Some of these exempted items have a 5% VAT; the rest, 0%. 

As a fraction of income, any VAT (not just Colombia's) falls more heavily on poorer households, because these spend a greater fraction of their income. Some of the exclusions appear intended to relieve the tax burden on lower income households: Bus rides, rent on a home, water, sewerage, and phone services, medical goods and services, and hundreds of kinds of food are subject to zero VAT. Other zero-VAT goods and services include payments associated with a second home, ocean travel, banking services, political contributions, and "espectaculos" such as ballet, cinema, theater, sporting events, circuses, and fairs.


# How we determined which populations carry how much of the VAT burden

## The Encuesta Nacional de Propuestos de Hogares (ENPH)

We used the ENPH, a survey of Colombian households conducted over 2016 and 2017. It picks a representative sample of homes, and then surveys everyone in the home, dividing them into "households", which are defined on the basis (income sharing? of whether they eat together?)

The ENPH is a big survey. We selected only a fraction of the data collected in it for use in this analysis. Those selections include:

* Data on goods and services: Each good or service the ENPH asks households about is identified by a COICOP code and a verbal description.
* Demographic data: Age, sex, race, education level, literacy, employment, and income.
* Purchase data:
  * What someone bought (as identified by its COICOP code)
  * How many
  * How often
  * What they spent on it


## Our COICOP-VAT match

Our other source of data is something we constructed ourselves. It associates a tax rate -- 0, 5 or 19% -- to each of the COICOP codes, based on the tax laws and the description of goods and services from the ENPH.


# What the data reveal

## What purchases look like

The survey records just under 7.5 million purchases. When people buy something, the median number they buy is 2. The maximum was a million, and the minimum -70 (yes, negative seventy). What they spent on each purchase ranges from 0 to 2.5 million pesos. We can calculate price by dividing what they spent by how many they were buying.

The survey includes a few categories for frequency of purchase. We translated those into numerical frequencies. A frequency of 30 indicates someone makes the same purchase 30 times in a month. That is the highest value. The least is .0027 -- once every two years.

Multiplying the value of a purchase by its frequency results in the amount of money someone spends on that good in a month, on average. It ranges from 0 to 23 million pesos, with an average of 34,000 and a median of 16,000.

The VAT paid on a purchase ranges from 0 to 4.4 million pesos. The average is 700 pesos. More than 3/4 of all purchases carry zero VAT -- which is plausible, given how many common purchases are exempt.


## What individuals look like

The 300,000 Colombians surveyed in the ENPH range in age from 0 to 110. Half are under 30. In education, only 5% indicate having less than a primary education; 45% indicate having completed primary or secondary and no further; 23% indicate "media", and 22% indicate having a university education. 53% of respondents are female. Incomes range from 0 to 80 million pesos per month, with a median of 800,000 -- just over the minimum wage. 30% of respondents are students. The number of transactions per person range from 1 to 144. [[Given that the minimum age is 0, the minimum number of purchases is strange.]]


## What households look like.

The average household has 3.37 members. The biggest has 22. The average number of purchases made by a household is 44 in a month; the minimum observed number is 1, and the maximum 358.

The age of the oldest person in a household ranges from 0 (who are they?) to 110. Half of households contain somebody over fifty. A quarter of households include someone under 5 years of age, and half include someone under 14. More than 3/4 of households include someone who has attained at least a "media" educational degree. 90% of households include at least one female member, and 86% at least one male. The minimum and maximum values for household income are little changed from their values for individuals; however the median is substantially higher -- 1.02 million as opposed to 800,000 for individuals. That difference seems likely to reflect the prevalence of households with one full-time earner and another part-time earner.


## Household spending and taxes

Average household spending is 1.5 million pesos per month. As a fraction of a household's income, that spending ranges from essentially zero to literally infinite, because so many households have zero income.

The rest of this analysis will exclude households with zero income. It will also discuss median values, rather than averages -- because while most households spend less than, say, ten times their income per month, some spend thousands of times more than their income, which skews the average.

Over half of income-receiving households spend more than their income.

The VAT falls more heavily on households with children, where a child is defined as a member younger than 18. Half of income-receiving households without children spend 0.8% of their income on the VAT; among households with children, that figure is 1.5%. If we replace "children" with "students" in that analysis, we find (to two decimal places) exactly the same result, presumably because the set of children and the set of students are nearly the same set.

The VAT also falls more heavily on households with an elderly member, defined as someone older than 65.

50% of households in which the most educated member has at least a university degree pay 0.8% or less of monthly income to the VAT. Half of other households pay at least 1.1%, unless their most educated member has less than a primary school education, in which case they pay 0.4% or less.


## Individual spending and taxes

Very few individuals in the youngest 20% of the population receive an income. In the next decile, though, there are many income earners. More than half of them spend less than 0.15% of their income on the VAT. In other deciles that fraction rises to about 0.3%.

VAT paid as a fraction of income varies widely across the races, from 0.13% to 0.51%. I can't say which races pay what, though, because the documentation codes them as 1-6, and in the data they range from 0 to 5.

The median male pays more than twice as much VAT, as a fraction of income, as the median woman.
