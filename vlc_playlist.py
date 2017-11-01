import json
import re
import sys

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<playlist version="1" xmlns="http://xspf.org/ns/0/">')
print('  <trackList>')

channels = json.load(sys.stdin)
for channel in channels:
    name = re.sub(r'[^\x20-\x7E]+', '', channel['name'])
    location = channel['location']

    print('    <track>')
    print('        <title>' + name + '</title>')
    print('        <location>' + location + '</location>')
    print('    </track>')

print('  </trackList>')
print('</playlist>')
