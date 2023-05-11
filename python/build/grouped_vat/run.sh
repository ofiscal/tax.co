# bash python/build/grouped_vat/run.sh

PYTHONPATH=$PYTHONPATH:"/mnt/tax_co"
code_folder=python/build/grouped_vat/

PYTHONPATH=$PYTHONPATH python3 $code_folder/1.coicop.py
PYTHONPATH=$PYTHONPATH python3 $code_folder/2.capitulo_c.py
PYTHONPATH=$PYTHONPATH python3 $code_folder/3.rename.py
PYTHONPATH=$PYTHONPATH python3 $code_folder/4.consumable_groups.py
