import json
import unicodecsv

outfile = open('../data/formatted.csv', 'wb')

infile = open('../data/parsed.json', 'r')

csvwriter = unicodecsv.writer(outfile)

csvwriter.writerow(['id', 'parent_id', 'author', 'date', 'title', 'content'])

for line in infile:
    data = json.loads(line)

    csvwriter.writerow([data['id' + ''], data['parent_id' + ''], data['author'],
                       data['date'], data['title'], data['content']])

infile.close()
