SHELL := bash
.PHONY: \
  input_subsamples \
  buildings


##=##=##=##=##=##=##=## Variables

##=##=##=##  Non-target variables

subsample?=1 # default value; can be overridden from the command line, as in "make raw subsample=10"
             # valid values are 1, 10, 100 and 1000
ss=$(strip $(subsample))# removes trailing space
python_from_here = PYTHONPATH='.' python3


##=##=##=##  Target variables

input_subsamples =                                                           \
  $(addsuffix .csv, $(addprefix data/enph-2017/recip-$(ss)/, $(enph_files))) \
  $(addsuffix .csv, $(addprefix data/enig-2007/recip-$(ss)/, $(enig_files)))

buildings = output/vat/data/recip-$(ss)/buildings.csv


##=##=##=##=##=##=##=## Recipes

##=##=##=## Build subsamples ofthe ENPH and the ENIG

input_subsamples: $(input_subsamples)
$(input_subsamples) : python/subsample.py $(enig_orig) $(enph_orig)
	$(python_from_here) python/subsample.py


##=##=##=## Build things from the ENPH

buildings: $(buildings)
$(buildings): $(input_subsamples) python/vat/build/buildings/main.py
	$(python_from_here) python/vat/build/buildings/main.py $(subsample)
