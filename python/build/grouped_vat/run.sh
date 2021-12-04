# bash python/build/grouped_vat/run.sh

PYTHONPATH="/mnt/tax_co":"/opt/conda/lib/python3.8/site-packages"
condaPython=/opt/conda/bin/python3

code_folder=python/build/grouped_vat/

PYTHONPATH=$PYTHONPATH $condaPython $code_folder/1.coicop.py
PYTHONPATH=$PYTHONPATH $condaPython $code_folder/2.capitulo_c.py
PYTHONPATH=$PYTHONPATH $condaPython $code_folder/3.rename.py
PYTHONPATH=$PYTHONPATH $condaPython $code_folder/4.consumable_groups.py
