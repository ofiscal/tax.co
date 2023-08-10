The ENPH classifies goods using two systems: "COICOP",
a European system with around 1400 categories,
and "Capitulo C", a system with only 30.
The latter is used to report grocery purchases in rural areas.
All other purchases use COICOP codes.

The microsimulation includes a few scattered spreadsheets
called `vat_by_capitulo_c` and `vat_by_coicop`.
These provide our estimates of which VAT rates apply to which goods.
Most of the so-named spreadsheets are not used,
but they are retained to understand the system's history.
The ones that are used are found in `config/vat/grouped/`.

These include some columns called "vat", "vat, min", and "vat, max".
These, too, are legacy -- we used to use them, and we don't any longer.
In the early days, each time we wanted to run a simulation,
someone would edit that spreadsheet by hand.
For most goods it was clear which VAT rate applied,
but for some, it was not; hence the three columns instead of one.

Also, the spreadsheets are somewhat wrongly named,
because in fact they include all the goods-specific taxes
that apply to each good.
So, for instance, because there's a special tax on restaurant food,
that VAT is not 0, 0.05 or 0.019.

When we put the simulation online, we reduced the resolution,
so to speak, of those VAT rates.
Rather than assign a distinct VAT to each good,
we assign a distinct VAT to each 2-digit coicop prefix.
There are only 14 of those, so this simplifies things a lot.
Moreover the categories are easy to explain to a user --
e.g. "food" or "medicine" --
so users have an easier time adjusting the tax code
to model anticipated changes.

However, as you'll notice in the simulation's online interface
(http://www.ofiscal-puj.org/microsim/run_make/manual_ingest),
there are other ways to adjust the VAT code,
via what I call "non-COICOP-based consumable groups".
Each good has exactly 1 2-digit COICOP prefix;
that is, the prefixes form a partition.
The non-COICOP-based consumable groups, such as "medicamentos"
or "infantiles", do not form a partition --
a medicine for babies, for instance, could be in both groups.

The COICOP spreadsheets identify, for each COICOP code,
not just its COICOP prefix,
but also whether or not it falls into each of the
non-COICOP-based groups consumable groups.

A user can assign any VAT they want to each of the prefixes.
By default there are only three -- 0, 0.05 and 0.019 --
but a user can define more.
Similarly, a user can assign any "bonus VAT"
to each of the non-COICOP-based consumable groups.

Moreover, both the COICOP-prefix-based consumable groups
and the non-COICOP-based consumable groups
can be assigned negative VAT values,
which correspond to subsidies.
