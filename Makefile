# PTIFALL: Whenever a file's imports are changed,
# `make/deps` needs to be updated to reflect that.

SHELL := bash

include make/phony
include make/variables
include make/deps
include make/tests
include make/build
