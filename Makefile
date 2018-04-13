SHELL := bash
.PHONY = all_fake_names all_enig_names
fake_names = a b
enig_names = Ig_gsdp_dias_sem.txt \
  Ig_gsdp_gas_dia.txt \
  Ig_gsdp_perceptores.txt \
  Ig_gsdu_caract_alim.txt \
  Ig_gsdu_dias_sem.txt \
  Ig_gsdu_gas_dia.txt \
  Ig_gsdu_gasto_alimentos_cap_c.txt \
  Ig_gsdu_mercado.txt \
  Ig_gs_hogar.txt \
  Ig_gsmf_compra.txt \
  Ig_gsmf_forma_adqui.txt \
  Ig_gsmf_serv_pub.txt \
  Ig_gssr_caract_alim.txt \
  Ig_gssr_gas_sem.txt \
  Ig_gssr_gasto_alimentos_cap_c.txt \
  Ig_gssr_mercado.txt \
  Ig_gs_vivienda.txt \
  Ig_ml_desocupado.txt \
  Ig_ml_hogar.txt \
  Ig_ml_inactivo.txt \
  Ig_ml_ocupado.txt \
  Ig_ml_pblcion_edad_trbjar.txt \
  Ig_ml_persona.txt \
  Ig_ml_vivienda.txt

all_fake_names: $(addprefix data/, $(fake_names))
$(addprefix data/, $(fake_names)):
	echo "hello" > $@

data/enig-2007/enig-2007.orig-txt.tgz:
	cd data; \
	  mkdir -p enig-2007; \
	  mv enig-2007.orig-txt.tgz enig-2007; \

all_enig_names: $(addprefix data/, $(enig_names))
$(addprefix data/, $(enig_names)): data/enig-2007/enig-2007.orig-txt.tgz
	cd data/enig-2007; \
	  tar -xvzf enig-2007.orig-txt.tgz
