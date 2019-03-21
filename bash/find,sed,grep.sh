# To avoid touching unmodified files:
for i in *;do grep mytext $i && sed -i -e 's/mytext/replacement/g' $i;done
  # https://stackoverflow.com/questions/27071019/sed-i-touching-files-that-it-doesnt-change

find . -name "*.py" -print0 | xargs -0 sed -i "s/prop.2018.11.31/prop_2018_10_31/g"

sed -i "s/python\/vat\/report/python\/report/g" Makefile

find . -name "*.py" -print0 | xargs -0 sed -i "s/python\/vat\/build/python\/build/g"
python/vat/build/

find . -name "*.py" -print0 | xargs -0 sed -i "s/contractor/independiente/g"

git diff | egrep -v "^.$" | egrep "^\+" | wc
  # count adds or deletes in the diff, ignore blank lines

find . -name "*.py" -print0 | xargs -0 grep -i "todo"

find . -name "*.py" -print0 | xargs -0 sed -ir "s/legends/purchase_file_legends/g"
find . -name "*~" -print0 | xargs -0 rm

find . -type f -print0 | xargs -0 egrep -v "\.dta|\.csv|\.zip|Ig_|st2_sea_enc|\.git"
