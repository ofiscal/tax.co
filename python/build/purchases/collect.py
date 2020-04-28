if True:
  import python.common.common as cl
  import python.build.output_io as oio
  #
  # input files
  import python.build.purchases.nice_purchases as nice_purchases
  import python.build.purchases.articulos      as articulos
  import python.build.purchases.capitulo_c     as capitulo_c


purchases = cl.collect_files(
  ( articulos.files
    # + medios.files
      # The tax only applies if the purchase is more than 880 million pesos,
      # and the data only records purchases of a second home.
    + capitulo_c.files
    + nice_purchases.files )
  , subsample = cl.subsample
)

oio.saveStage(cl.subsample, purchases, 'purchases_0')

