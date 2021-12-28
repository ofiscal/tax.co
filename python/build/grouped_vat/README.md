# About the "vat", "vat, min" and "vat, max" columns

The tax laws do not precisely conform to the COICOP labeling of goods.
We (especially our tax policy expert, David Suarez) had to exercise judgment,
determining which VAT rate applied to which COICOP category.
In some cases the VAT was clear.
For those cases in which it was not,
we recorded what we believed were conservative
(i.e. wide) minimum and maximum possible VAT values.

In 2021 we decided to collapse a lot of that detail,
and assigned a simple VAT equal to the average
of the min and max VAT values from 2018/2019.
See python/build/grouped_vat/*.py, searching for "vat, min", for details.
