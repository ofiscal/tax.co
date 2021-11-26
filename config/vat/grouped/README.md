`1.dos2unix/` contains the nearly-raw data Daniel Duque sent me
(on Nov 2021), created by him and Valentina Herrera Ospina.
(That folder starts with a `1` to distinguish it from `0.raw`,
which is the literal raw data, and differs from `1.dos2unix/`
only in that the latter has been processed by `dos2unix`
to remove Windows-style line terminators.)

The data from `1.dos2unix` was processed
(outside of the make-coordinated build chain)
by `python/build/grouped_vat*.py`,
and written to the top level of this folder.

PITFALL: That new data is *substantially different* from
the earlier data above it.
For the few goods in which "vat, min" != "vat, max",
it defines "vat" to be their average,
whereas before "vat" was undefined.
Also, of course, it has new columns like "prefix" or "pink tax"
which were never contemplated for the earlier data set.
The "prefix vat" rate is computed by averaging
the "vat" column of all the goods with a given prefix.
