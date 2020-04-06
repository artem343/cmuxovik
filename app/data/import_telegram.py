# To add a new cell, type ' '
# To add a new markdown cell, type '  [markdown]'

import json
import bs4

SOURCE = 'telegram'

with open('telegram_messages.html', 'r') as f:
    contents = f.read()

soup = bs4.BeautifulSoup(contents, 'lxml')

soup.find(class_=['default'])  # One post
message = soup.find(class_=['default'])
body = message.find(class_='body')
time = body.find(class_='date')['title']
author = body.find(class_='from_name').text.strip()
text = body.find(class_='text').text.strip()

cmuxes = []

for cmux in soup.find_all(class_=['default']):
    try:
        body = cmux.find(class_='body')
        time = body.find(class_='date')['title']
        author = body.find(class_='signature').text.strip()
        cs = body.find(class_='text').contents
        text = "\n".join([c for c in cs[::2]]).strip()
        d = {
            'time': time,
            'author': author,
            'text': text,
            'source': SOURCE
        }
        cmuxes.append(d)
    except Exception:
        pass


with open('telegram_messages.json', 'w', encoding='utf8') as json_file:
    json.dump(cmuxes, json_file, ensure_ascii=False)
