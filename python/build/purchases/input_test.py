if True:
  import python.build.classes as cla
  import python.build.output_io as oio
  import python.build.purchases.articulos as articulos
  import python.build.purchases.capitulo_c as capitulo_c
  # import python.build.purchases.medios as medios
  import python.build.purchases.nice_purchases as nice_purchases
  import python.common.util as util
  import python.common.common as common


def test_purchase_inputs():
  for f in ( articulos.files
         # + medios.files
           + capitulo_c.files
           + nice_purchases.files
           ): 
    df = common . retrieve_file (
        f,
        subsample = 1 ) # PITFALL: Always the full sample.
    assert util.unique( df.columns )
    acc = {}
    for c in df.columns:
      acc.update( [ (c, cla.stringProperties( df[c] ) ) ] )
      assert acc[c] == cla.input_map( f.col_specs )[c]


if True: # run tests
  log = "starting\n"
  test_purchase_inputs()
  for ss in common . valid_subsamples:
    # PITFALL: Looping over subsample sizes because this program
    # always uses the full sample.
    # If it works, it works for all subsamples.
    oio.test_write( subsample = ss
                  , filename = "purchase_inputs"
                  , content = log )
