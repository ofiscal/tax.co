enph_folders = Caracteristicas_generales_personas                         \
  Gastos_diarios_del_hogar_Urbano_-_Comidas_preparadas_fuera_del_hogar	  \
  Gastos_diarios_personales_Urbano					  \
  Gastos_diarios_Urbanos						  \
  Gastos_diarios_Urbanos_-_Mercados					  \
  Gastos_menos_frecuentes_-_Articulos					  \
  Gastos_menos_frecuentes_-_Medio_de_pago				  \
  Gastos_personales_Rural						  \
  Gastos_personales_Rural_-_Comidas_preparadas_fuera_del_Hogar		  \
  Gastos_personales_Urbano_-_Comidas_preparadas_fuera_del_hogar		  \
  Gastos_semanales_Rural_-_Capitulo_C					  \
  Gastos_semanales_Rural_-_Comidas_preparadas_fuera_del_hogar		  \
  Gastos_semanales_Rurales						  \
  Gastos_semanales_Rurales_-_Mercados					  \
  Viviendas_y_hogares

all = $(addprefix csv/, $(addsuffix .csv, $(enph_folders))) \
      $(addprefix dta/, $(addsuffix .dta, $(enph_folders))) \
      $(addprefix sav/, $(addsuffix .sav, $(enph_folders)))

$(all): ENPH-2016-official.tar.gz
	mkdir csv dta sav
	mkdir temp-for-unpacking
	cd temp-for-unpacking                      ; \
	  mv ../ENPH-2016-official.tar.gz .	   ; \
	  tar -xvzf ENPH-2016-official.tar.gz	   ; \
	  mv */*.csv ../csv			   ; \
	  mv */*.dta ../dta			   ; \
	  mv */*.sav ../sav			   ; \
	  mv README* ENPH-2016-official.tar.gz ..  ; \
	  rmdir $(enph_folders)
	rmdir temp-for-unpacking
	mkdir orig
	mv csv dta sav orig

        # replace tab with semicolon, to make these like the others
	sed -i -r "s/\t/\;/g" orig/csv/Gastos_menos_frecuentes_-_Articulos.csv \
                              orig/csv/Gastos_diarios_Urbanos.csv
