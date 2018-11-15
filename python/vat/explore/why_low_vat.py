
import python.build.output_io as oio
import python.util as util

subsample = 10
purchases = oio.readStage( subsample, "purchases_2_vat" )

util.describeWithMissing( purchases[[ "25-broad-categs", "coicop" ]] )
