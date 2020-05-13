# PITFALL: Where you find `$$` written below, it's Makefile-specific syntax.
# In bash, you would write it with a single $.
# In a Makefile, though, where you write a single $,
# the variable substitution is performed by make before reaching bash.
# If you want to wait until the expression reaches bash before substituting,
# you need to use $$.

SHELL := bash
.PHONY = verify unpack_and_rename handle_txt_files

data:			\
  verify		\
  unpack_and_rename	\
  verify_txt		\
  move_txt		\
  format_csv

verify: # verify the content of the raw zipfiles
	echo "If this fails, checksum does not match value expected as of 2019 07 03."
	sha1sum 1_raw/* | sort | sha1sum | grep "89f4fbad99d66a4ebfd130694e9052536cec55ea"

# PITFALL: The files ending inn .csv here are not in fact comma-separated. Instead,
#          they are semicolon-separated, so I rename them from *.csv to *.ssv.
unpack_and_rename: verify
	# Without the next line, the unzip fails later.
	cd 1_raw							; \
	  for x in *.zip; do mv -- "$$x" "$${x// /_}"; done
	mkdir -p 2_unzipped
	cd 2_unzipped							; \
	  for a in `ls -1 ../1_raw/*.zip`; do unzip "$$a"; done		; \
	  for x in *.*; do mv -- "$$x" "$${x// /_}"; done		; \
	  for x in *.csv; do mv -- "$$x" "$${x//\.csv/.ssv}"; done	; \
	  mkdir -p ssv dta sav						; \
	  mv *.ssv ssv							; \
	  mv *.dta dta							; \
	  mv *.sav sav
	cd 1_raw							; \
	  for x in *.zip; do mv -- "$$x" "$${x//_/ }"; done # undo changes to raw data
          # PITFALL: This last step, the undoing, depends on the fact that the filenames
	  # in the raw DANE data contain no underscores.

# If there are no quotation marks in the .txt files,
# replace tab with semicolon, change .txt to .csv,
# and move to where the other .ssv files are.
verify_txt:
	cd 2_unzipped									; \
	  touch definitely_empty							; \
	  grep "'|\"" *.txt > hopefully_empty						; \
	  cmp -s hopefully_empty definitely_empty					; \
	  if cmp -s hopefully_empty definitely_empty					; \
	    then echo "Good: No single or double quotation marks found in *.txt."	; \
	    else echo "Trouble: Single or double quotation marks found in *.txt."	; \
	         exit 1									; \
	  fi										; \
	  rm hopefully_empty definitely_empty

move_txt:
	cd 2_unzipped							; \
	  sed -i -r "s/\t/\;/g" *.txt					; \
	  for x in *.txt; do mv -- "$$x" "$${x//\.txt/.ssv}"; done	; \
	  mv *.ssv ssv							; \

# PITFALL: `csvtool` deletes whitespace between separators.
# This is potentially confusing, but good,
# as it causes the missing value to be read as NaN rather than " ".
# PITFALL: `csvtool` converts numbers containing commas to strings.
# Those value are handled downstream, in the Python code.
format_csv:
	mkdir 3_csv
	cd 2_unzipped/ssv					; \
	  for i in *; do					  \
	    csvtool -t ';' -u ',' cat $$i -o ../../3_csv/$$i	; \
	  done
	cd 3_csv						; \
	  for x in *.ssv; do					  \
	    mv -- "$$x" "$${x//\.ssv/.csv}"			; \
	  done
