# PITFALL: Files here must be kept in sync with some files elsewhere

The file
  `config/vat/grouped/consumable_groups_by_coicop.csv`
defines, for each two-digit COICOP prefix,
the default values that appear in the web interface
Those should be the same as the default values used by the baseline simulation,
which is defined in
  `users/symlinks/baseline/vat/grouped/consumable_groups_by_coicop.csv`.

A similar concern applies to the other VAT groups we define.

*And* the same concern applies to marginal income tax rates.
However, in that case there is an easy fix: If they ever go out of sync,
just run the following from the project's root:

  baseline_for_sim=users/symlinks/baseline/config/marginal_rates
  baseline_for_webui=config/marginal_rates
  cp $baseline_for_sim/*.csv $baseline_for_webui


# Main text, kind of stale

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
Also, of course, it has new columns like "prefix" or "impuesto rosa"
which were never contemplated for the earlier data set.
The "prefix vat" rate is computed by averaging
the "vat" column of all the goods with a given prefix.
