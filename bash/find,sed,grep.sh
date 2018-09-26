find . -name "*.py" -print0 | xargs -0 grep -i "todo"

find . -name "*.py" -print0 | xargs -0 sed -ir "s/legends/purchase_file_legends/g"
find . -name "*.pyr" -print0 | xargs -0 rm

find . -type f -print0 | xargs -0 egrep -v "\.dta|\.csv|\.zip|Ig_|st2_sea_enc|\.git"
