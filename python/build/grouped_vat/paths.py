from os.path import join


folder_grouped_vat  = "config/vat/grouped/"
folder_dos2unix     = join ( folder_grouped_vat,
                             "1.dos2unix" )

file_vat_cap_c_raw  = join ( folder_dos2unix,
                             "vat-by-capitulo-c.tsv" )
file_vat_cap_c      = join ( folder_grouped_vat,
                             "vat_by_capitulo_c.csv" )

file_vat_coicop_raw = join ( folder_dos2unix,
                             "vat-by-coicop.tsv" )
file_vat_coicop     = join ( folder_grouped_vat,
                             "vat_by_coicop.csv" )

file_vat_dicc_raw   = join ( folder_dos2unix,
                             "dicc_coicop.tsv" )
file_vat_dicc       = join ( folder_grouped_vat,
                             "dicc_coicop.csv" )
