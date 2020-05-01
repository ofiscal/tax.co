These are 1/10 results.

There are almost 9000 households in the 1/10 subsmample, of whom fewer than 600 used savings and only 23 bought a house that month:

>>> len(hh)
8720
>>> len( hh[ hh["used savings"] > 0 ] )
565
>>> len( hh[ hh["recently bought this house"] > 0 ] )
23

These are the deciles for the number of months it would take to save for a month.

full sample
0.0 0.0
0.1 0.17263291398466188
0.2 0.402974454196375
0.3 0.7857525546355124
0.4 1.6253761644395586
0.5 5.006090280058862
0.6 10000.0
0.7 10000.0
0.8 10000.0
0.9 10000.0
1.0 10000.0

The ten-thousand value is inaccurate. The algorithm I used computes the "months it would take to save for a month" variable like this:

    if spending >= income:
        return 1e4
    else: return spending / (income - spending)

That is, if someone's spending is greater than or equal to their income, it's impossible for them to save any money. I put ten thousand because infinity is not a value understood by some parts of Pandas.

The selective sample (next) gives results almost indistinguishable from the full sample. In addition to the mathematical reasons to expect that, there's a data reason -- while the COICOP system includes a code for "compra de vivienda", it appears nowhere in the ENPH data, so even if someone bought a house, it appears that the ENPH does not record the expense. (Actually they do record it, in the Vivienda data set rather than the purchase data set(s). But anyway it doesn't affect these results.

nobody who bought a house or used savings
0.0 0.0
0.1 0.17046935659797707
0.2 0.4028162148782592
0.3 0.7913500356726448
0.4 1.6474147671581263
0.5 5.11142468919852
0.6 10000.0
0.7 10000.0
0.8 10000.0
0.9 10000.0
1.0 10000.0

Despite the fact that this suggests half of Colombia is incapable of saving, I'm still surprised at the optimism of these results. They indicate that more than 20% of Colombia saves more than 2/3 of their income (i.e. they can save for a month in less than half a month).

We include two kinds of income, cash and in-kind. It occurred to me that maybe in-kind income does not show up in the purchase data, making it look like people consume less than they do. So I tried using only cash income instead of all income. The results don't really change:

 full sample , all income
0.0 0.0
0.1 0.17263291398466188
0.2 0.402974454196375
0.3 0.7857525546355124
0.4 1.6253761644395586
0.5 5.006090280058862
0.6 10000.0
0.7 10000.0
0.8 10000.0
0.9 10000.0
1.0 10000.0

 full sample , cash income
0.0 0.0
0.1 0.17437524373432803
0.2 0.40919113378391814
0.3 0.7975120805884222
0.4 1.6564104762416898
0.5 5.2711043589517335
0.6 10000.0
0.7 10000.0
0.8 10000.0
0.9 10000.0
1.0 10000.0

 nobody who bought a house or used savings , all income
0.0 0.0
0.1 0.17046935659797707
0.2 0.4028162148782592
0.3 0.7913500356726448
0.4 1.6474147671581263
0.5 5.11142468919852
0.6 10000.0
0.7 10000.0
0.8 10000.0
0.9 10000.0
1.0 10000.0

 nobody who bought a house or used savings , cash income
0.0 0.0
0.1 0.17209213498081777
0.2 0.4080775495389354
0.3 0.8069245052743264
0.4 1.6683340959903297
0.5 5.373887908329267
0.6 10000.0
0.7 10000.0
0.8 10000.0
0.9 10000.0
1.0 10000.0

Last I tried restricting to households with more than 2 members. The situation looks worse for them, but very similar:

 3 or more members , all income
0.0 0.0
0.1 0.23710588273640593
0.2 0.5202274233330617
0.3 1.032699831651648
0.4 2.2716894993056864
0.5 9.872719229005071
0.6 10000.0
0.7 10000.0
0.8 10000.0
0.9 10000.0
1.0 10000.0

 3 or more members , cash income
0.0 0.0
0.1 0.24001910329513979
0.2 0.5274967073247481
0.3 1.0426311412922695
0.4 2.3201784787006696
0.5 11.078278598070467
0.6 10000.0
0.7 10000.0
0.8 10000.0
0.9 10000.0
1.0 10000.0

If you were interested in other specific demographics, there are lots of other subsets I could run through the same process.
