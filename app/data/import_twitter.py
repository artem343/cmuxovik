# To add a new cell, type ' '
# To add a new markdown cell, type '  [markdown]'

import json
import bs4
import csv
import datetime

SOURCE = 'twitter'

with open('stih_twitter.txt', 'r') as f:
    read_tsv = csv.reader(f, delimiter="\t")

    cmuxes = []
    for row in read_tsv:
        if(len(row) == 3):
            date_obj = datetime.datetime.strptime(row[0].strip(), "%Y-%m-%d")
            d = {
                'time': date_obj.strftime('%d.%m.%Y %H:%M:%S'),
                'author': row[2].strip(),
                'text': row[1].strip(),
                'tag': '',
                'source': SOURCE
            }
            cmuxes.append(d)
    print(cmuxes[0])

with open('twitter_cmuxes.json', 'w', encoding='utf8') as json_file:
    json.dump(cmuxes, json_file, ensure_ascii=False)
