How to build and run the Encuesta Nacional de Presupuestos de Hogares.

# Step 1: Download the data

The raw microdata used in tax.co is the ENPH. It comes from DANE.
You can find it
[here](http://microdatos.dane.gov.co/index.php/catalog/566/get_microdata).

# Step 2: Place the data

In this project, the folder `data/enph-2017/`
initially contains only a `Makefile`.
Once you have downloaded the raw data (16 .zip files) from DANE,
put it in a new folder called `data/enph-2017/1_raw`,
right next to the `Makefile` and this `README.md` file.

# Step 3: Use the Makefile to clean the data

If you don't have `make` installed, install it.
Go to `tax.co/data/enph-2017/`.
Run `make data`.

This will extract the contents of the two you downloaded,
rename them as needed,
fix some separator inconsistencies,
and move them into some new, appropriately-structured folders.
