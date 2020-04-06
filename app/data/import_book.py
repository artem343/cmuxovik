# To add a new cell, type ' '
# To add a new markdown cell, type '  [markdown]'

import json
import bs4

SOURCE = 'book'

with open('stih.txt', 'r') as f:
    filetext = f.readlines()

cmux_tuples = []
cur_cmux = ''
for line in filetext[4:]:
    if line.isupper():
        cur_tag = line.strip()
    elif line == '\n':
        if cur_cmux != '':
            cmux_tuples.append((cur_cmux.strip(), cur_tag.lower()))
            cur_cmux = ''
    else:
        cur_cmux = cur_cmux + line

cmuxes = []
for t in cmux_tuples:
    d = {
        'time': '01.04.2015 17:00:00',
        'author': '',
        'text': t[0],
        'tag': t[1],
        'source': SOURCE
    }
    cmuxes.append(d)


with open('book_cmuxes.json', 'w', encoding='utf8') as json_file:
    json.dump(cmuxes, json_file, ensure_ascii=False)
