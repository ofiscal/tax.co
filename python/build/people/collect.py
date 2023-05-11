# From the raw ENPH person-level data,
# creates a data set that's a little friendlier.

if True:
  import python.build.output_io as oio
  import python.build.people.files as files
  import python.common.common as cl
  import python.common.misc as c


ppl = c.all_columns_to_numbers (
  cl.collect_files ( files.files,
                     subsample = cl.subsample ),
  skip_columns = ["non-beca sources"] # PITFALL : a space-separated list of ints
)

oio.saveCommonOutput ( cl.subsample, ppl, 'people_0')
