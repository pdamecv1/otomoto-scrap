#!/usr/bin/env

echo $ENV
echo $(env | grep -i POSTGRES)
python otomoto_scrapper.py && python db-sync.py

# For debug
tail -f /dev/null