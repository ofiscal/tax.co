##### What this does #####
#
# It lets you run overview_lag.sh and python/test/overview_diff.py.
# It's for determining whether changes to the code have resulted
# in changes to the overview.py file.


##### Workflow (how to use it) #####
#
# (0) Decide which arguments will be used in make-all-models.sh.
# Modify this file to consider the same arguments.
# (That modification may involve introducing loops here,
# to match the ones there.)
#
# (1) Run the "make lag" line below,
# to copy the current overview file to the corresponding "prev" folder.
#
# (2) Modify the code. Execute it as much as needed until it seems to work
# -- including having generated a new "overview" file.
#
# (4) Run the "make diff" line below. Check for red text.


make lag  subsample=100 strategy=detail
make diff subsample=100 strategy=detail
