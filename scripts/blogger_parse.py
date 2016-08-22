import json
import os
from collections import OrderedDict

with open('../data/raw.json', 'r') as json_data:
    d = json.load(json_data)

json_data.close()

rawData = d['items']

all_data = []

# print(rawData)
outfile = open('../data/parsed.json', 'w')

for each in rawData:
    line = dict()
    line['id'] = each['id']
    line['parent_id'] = ''
    line['author'] = each['author']['displayName']
    line['date'] = each['published']
    line['title'] = each['title']
    line['content'] = each['content']
    # all_data.append(line)
    outfile.write(json.dumps(line) + '\n')

    try:
        for item in each['replies_body']:
            reply = dict()
            reply['id'] = item['id']
            reply['parent_id'] = item['post']['id']
            reply['author'] = item['author']['displayName']
            reply['date'] = item['published']
            reply['title'] = ''
            reply['content'] = item['content']
            # all_data.append(reply)
            outfile.write(json.dumps(reply) + '\n')
    except:
        pass

outfile.close()
