Sometimes numbers in Spanish are formatted using a comma (,) as the decimal point, and a period (.) to indicate powers of 1000 (as in 1.000 = 1 thousand, or 1.000.000 = 1 million).

The code at `python/prelim-explore/spanish-num/` generates evidence (described below) useful for determining whether swapping commas for periods in numbers is in fact a problem, at least for the columns of the ENPH-2017 used in the VAT analysis.

That code detects no such formatting errors within the data. However, there could be such problems upstream, in the processes at DANE that generated the data.

It is, however, still possible that, e.g., the number 1000 was input as 1.000 into the software that produced the ENPH before we received it.


# The "Spanish number format problem" may have distorted the process of creating the ENPH

One thing that [this program](python/prelim-explore/spanish-num/enph-2017/fractions.py) does is calculate, for each numeric column used in the VAT analysis, the minimum nonzero value in that column. It outputs, in relevant part, the following:

```
value's minimum positive value: 
1.0
value(credit)'s minimum positive value: 
98.0
value(total/cash)'s minimum positive value: 
31.0
```

That seems to indicate a problem, because units of Colombian currency less than 50 pesos are not in use.


# Internally, the ENPH does not exhibit the "Spanish number format problem"

If a column has any cell with a value with a comma in it, it is interpreted as a string, not a number -- but all the columns we want read as numbers are indeed read that way. Ditto if a column has a cell with two periods.

If the column has only one period, one cannot tell without more information whether it's n using that period as a decimal point or a power-of-1000 indicator. However, when I read the data and compute the remainder of each column after subtracting the floor of the value there, every column except "quantity" produces a series of nothing but zeroes. That is to say, the original values were integers. (A fractional "quantity" value seems acceptable; what would have been bad is a fractional price, since nobody uses less than 50 pesos at a time.)

If the data had any value intending to represent a multiple of 1000 that ended in ".000", it would be read as a floating-point value with no fractional part, and thus not detected by the previous test. To make sure that was not happening, I read the data used by the VAT calculation (from the 1/10 sample) as text, and then output that as another .csv file. I then searched that file for any instance of the string ".000". There were a lot -- but they were all part of dates. When I exclude the regular expression "\:..\.000" (that is, a colon, followed by any two characters (I could have said any two digits), followed by a period, followed by three zeroes) I find none.
