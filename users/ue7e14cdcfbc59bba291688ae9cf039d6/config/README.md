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

# What this is

This (`baseline/`) is not a user-generated "user".
Rather, it is a default configuration,
to be used as a baseline for comparison.

The `.py` files are generated dynamically from the similarly-named `.csv` files,
using the code at `haskell/MarginalTaxRates/`.
