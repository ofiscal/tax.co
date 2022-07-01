######### What this is #########
# This is NOT a script, but rather a collection of handy one-liners,
# for various common tasks like renaming variables.

exit # To make sure you don't run this as a script.

# To grep for a string in every format except tables and unreadable ones.
find . -type f -not \( -name "*.csv" -o -name "*.xlsx" -o -name "*.tgz" -o -name "*.zip" -o -name "*.ssv" -o -name "*.sav" -o -name "*.pyc" -o -name "*.pdf" -o -name "*.jpeg" -o -name "*.odt" -o -name "*.pack" -o -name "*.ods" -o -name "*.ipynb" -o -name "*.idx" -o -name "*.docx" -o -name "*.dta" \) -print0 | xargs -0 grep "xxx" --color

# Always using: Find multiple files, replace in them
find . \( -name "*.py" -o -name "*.md" -o -name "*.org" \) -print0 | xargs -0 sed -i "s/prop.2018.11.31/prop_2018_10_31/g"

# Find and replace without touching unmodified files.
# (Otherwise `make` acts as if everything needs to be rerun.)
# https://stackoverflow.com/questions/27071019/sed-i-touching-files-that-it-doesnt-change
for i in *; do grep mytext $i && sed -i -e 's/mytext/replacement/g' $i; done

# Find and replace in all files.
find . -name "*.py" -print0 | xargs -0 sed -i "s/prop.2018.11.31/prop_2018_10_31/g"

# find all files in a certain set of types (file extensions)
find . -regex ".*\.\(yaml\|txt\)"

# Find and replace.
sed -i "s/python\/vat\/report/python\/report/g" Makefile

# Count lines added or deleted in the diff, ignore blank lines.
# (This is the sum of additions and subtractions, not their difference.)
git diff | egrep -v "^.$" | egrep "^\+" | wc

# Find in all files of one particular type.
grep -i "todo" -r . --include="*.py"
# Find (case-insensitive) in all files of many types
find . -regex ".*\.\(py\|txt\|sh\|org\|mm\|md\|hs\)" -print0 | xargs -0 grep -i "todo"

# Delete all files ending in "~" (the suffix on backups).
find . -name "*~" -print0 | xargs -0 rm

# Find multiple patterns
find . \( -name "*.py" -o -name "*.md" -o -name "*.org" \)
