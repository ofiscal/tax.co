# PTIFALL: Whenever a file's imports are changed,
# `make/deps` needs to be updated to reflect that.

SHELL := bash

include make/Makefile.phony
include make/Makefile.variables
include make/Makefile.deps
include make/Makefile.tests
include make/Makefile.build
