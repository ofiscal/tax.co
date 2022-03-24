# WHAT IT DOES:
# For each user folder,
# prints its size, the time it was last modified,
# and its config.json file
# (in particular, the user's email address).

# HOW IT WORKS:
# `printf` prepends modification time in seconds.
# `egrep -v` discards the folders "." and "symlinks".
# `awk` keeps the user folder (stripping the modification time).
# `sed` discards the first two characters,
# which are all `./`
# and interfere with the `grep` in the loop.

for u in $(find . -maxdepth 1 -type d -printf "%T@ %p\n" | sort | egrep -v "symlinks|\.$" | awk '{print $2}' | sed 's/^..//'); do
    echo ""
    du -hs $u
    ls -l | grep -i $u
    cat $u/config/config*
    echo ""
done
