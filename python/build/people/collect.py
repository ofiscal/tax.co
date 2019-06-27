import python.build.output_io as oio
import python.build.people.files as files
import python.common.cl_args as cl
import python.common.misc as c


ppl = c.all_columns_to_numbers(
  cl.collect_files( files.files
                  , subsample = cl.subsample )
  , skip_columns = ["non-beca sources"] # PITFALL : a space-separated list of ints
)

oio.saveStage(cl.subsample, ppl, 'people_0')
