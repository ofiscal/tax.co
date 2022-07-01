# Purpose
These functions return triples that encode
how to determine someone's income tax as a function of their wage.
Interpret those triples as follows:
1. Number: threshold at which a new income tax rate takes effect.
2. Taxable base. This is a function; you input someone's wage,
   and it outputs the amount of that money subject to the tax.
3. Average tax rate.

# PITFALL
The ENPH data gives nominal salary, before any of these contributions.

# PITFALL
Contractors pay all income taxes themselves. Employees do not --
they pay some part of those taxes themselves,
and their employer pays the rest.
(In an economic sense, it all comes out of the employee's wages,
but in a legal sense, the burden is shared with the employer.)

# Context
The model `rentas_naturales.xlsx` might make this easier to understand.
