SHELL := bash
.PHONY = verify unpack_and_rename handle_txt_files

data: \
  verify \
  unpack_and_rename \
  handle_txt_files

verify: # verify the content of the raw zipfiles
	echo "If this fails, checksum does not match value expected as of 2019 07 03."
	sha1sum 1_raw/* | sha1sum | grep "bd8c4db51854716c860c2cac797a677d41f7b83d"

unpack_and_rename:
	# Without the next line, the unzip fails later.
	cd 1_raw						; \
	  find . -name "*.zip" | rename 's/ /_/g'
	mkdir -p 2_unzipped
	# PITFALL: In bash rather than make, one would use $ (not $$) below.
	cd 2_unzipped						; \
	  for a in `ls -1 ../1_raw/*.zip`; do unzip "$$a"; done ; \
	  mkdir -p csv dta sav					; \
	  mv *.csv csv						; \
	  mv *.dta dta						; \
	  mv *.sav sav						; \
	  find -regex ".*\.\(sav\|csv\|dta\|txt\)" | rename 's/ /_/g'
	cd 1_raw						; \
	  find . -name "*.zip" | rename 's/_/ /g' # undo changes to raw data

# If there are no quotation marks in .txt files,
# replace tab with semicolon, change .txt to .csv,
# and move to where the other .csv files are.
handle_txt_files:
	cd 2_unzipped								  ; \
	  touch definitely_empty						  ; \
	  grep "'|\"" *.txt > hopefully_empty					  ; \
	  cmp -s hopefully_empty definitely_empty				  ; \
	  if cmp -s hopefully_empty definitely_empty				  ; \
	    then echo "Good: No single or double quotation marks found in *.txt." ; \
	    else echo "Trouble: Single or double quotation marks found in *.txt." ; \
	         exit 1                                                           ; \
	  fi									  ; \
	  sed -i -r "s/\t/\;/g" *.txt						  ; \
          find -regex ".*\.txt" | rename 's/\.txt/\.csv/g'			  ; \
	  mv *.csv csv								  ; \
	  rm hopefully_empty definitely_empty
