# This shows all CSV files with a column named $TARGET.

TARGET="vacaciones" # a substring of the column name you want to search for

head -n 1 *.csv | grep -B 1 $TARGET  | grep ".csv <==$"
