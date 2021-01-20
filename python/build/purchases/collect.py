if True:
  import python.common.common as com
  import python.build.output_io as oio
  import python.common.misc as misc
  import python.common.util as util
  #
  # input files
  import python.build.purchases.nice_purchases as nice_purchases
  import python.build.purchases.articulos      as articulos
  import python.build.purchases.capitulo_c     as capitulo_c


purchases = com . collect_files(
  ( articulos.files
    # + medios.files
      # The tax only applies if the purchase is more than 880 million pesos,
      # and the data only records purchases of a second home.
    + capitulo_c.files
    + nice_purchases.files )
  , subsample = com.subsample
)

assert util.near(
    # PITFALL: This differs from the usual idiom which separates testing
    # from production. That's because the only thing tested here is
    # the number of rows; reading the entire data set into memory again
    # for such a simple test seems unworth the added execution time.
    len ( purchases ),
    misc . num_purchases / com . subsample,
    tol_frac = (
        1 / 20 if not com . subsample == 10
        else 1 / 2 ) )
# TODO | BUG? Why is the previous conditional necessary? That is, why,
# in the special case of subsample = 1/10, is the size of the
# purchase data so different from what you'd expect.
# This isn't necessarily wrong, since the data is subsampled by households,
# and households can make different numbers of purchases.
# That's why `tol_frac` needs to be substantial in both cases.
# But it's surprising, because for subsample = 10,
# the reality is much less than the expectation.

oio.saveStage( com.subsample, purchases, 'purchases_0' )
