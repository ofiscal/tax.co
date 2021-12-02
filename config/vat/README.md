The first data were these:
```
vat_by_capitulo_c.csv
vat_by_coicop.csv
```

In those two files there are three VAT columns: min, max, and "the" VAT. The min and max are what the Observatorio deduced based on the laws of Colombia. "The" VAT column is only defined where the min and max are equal. It was not used in the original analysis.

The data in the `fake_grouped/` folder are fake.

The real grouped data include extra binary (0 or 1)
columns that define groups of goods, such as "for babies" or "alcohol".
Some of them overlap.
Each good falls in at least one category,
because some of the categories are defined based on the first two digits of the coicop code.
