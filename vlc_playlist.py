import json, re

data_file = open('results_json.txt', 'r')
channels = json.load(data_file)

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<playlist version="1" xmlns="http://xspf.org/ns/0/">')
print('  <trackList>')

for channel in channels:
    name = re.sub(r'[^\x20-\x7E]+','', channel['name'])
    location = channel['location']

    print('    <track>')
    print('        <title>' + name + '</title>')
    print('        <location>' + location + '</location>')
    print('    </track>')

print('  </trackList>')
print('</playlist>')
