`1.dos2unix/` contains the nearly-raw data Daniel Duque sent me
(on Nov 2021), created by him and Valentina Herrera Ospina.
(That folder starts with a `1` to distinguish it from `0.raw`,
which is the literal raw data, and differs from `1.dos2unix/`
only in that the latter has been processed by `dos2unix`
to remove Windows-style line terminators.)

The data from `1.dos2unix` was processed
(outside of the make-coordinated build chain)
by `python/build/grouped_vat.py`,
and written to the top level of this folder.
