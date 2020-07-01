How to build and run the Encuesta Nacional de Presupuestos de Hogares.

# Get the data

The raw microdata used in tax.co is the ENPH. It comes from DANE.
You can find it
[here](http://microdatos.dane.gov.co/index.php/catalog/566/get_microdata).

In this project, the folder `data/enph-2017/`
initially contains only a `Makefile`.
Once you have downloaded the raw data (16 .zip files) from DANE,
put it in a new folder called `data/enph-2017/1_raw`,
right next to the `Makefile`.

# Clean the data

This will extract the contents of the two archives you downloaded,
rename them as needed,
fix some separator inconsistencies,
and move them into some appropriately-structured folders.

Go to `tax.co/data/enph-2017/`.
If you downloaded the data from DANE, run `make data_from_dane`.
If you downloaded the data from Javeriana, run `make data_from_puj`.
