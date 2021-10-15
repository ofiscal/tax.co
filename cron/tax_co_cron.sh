# PITFALL: The `config.json` argument is ignored
# when the last argument is `try-to-advance-queue`,
# but still must be supplied.

cd /mnt/tax_co
export PYTHONPATH=/mnt/tax_co:$PYTHONPATH
/opt/conda/bin/python3      \
    python/requests/main.py \
    config/config.json      \
    try-to-advance-queue    \
    >> requests-cron-log.txt 2>&1
