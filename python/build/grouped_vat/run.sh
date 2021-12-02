# bash python/build/grouped_vat/run.sh

PYTHONPATH="/mnt/tax_co":"/opt/conda/lib/python3.8/site-packages"
condaPython=/opt/conda/bin/python3

PYTHONPATH=$PYTHONPATH $condaPython python/build/grouped_vat/1.coicop.py
PYTHONPATH=$PYTHONPATH $condaPython python/build/grouped_vat/2.capitulo_c.py
PYTHONPATH=$PYTHONPATH $condaPython python/build/grouped_vat/3.rename.py
