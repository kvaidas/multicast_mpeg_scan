import json
import re
import sys

# Load DB file with the channels
with open('channel_db.json') as db_file:
    db = json.load(db_file)

# Print playlist header
print('<?xml version="1.0" encoding="UTF-8"?>')
print('<playlist version="1" xmlns="http://xspf.org/ns/0/">')
print('  <trackList>')

# Iterate over available channels
for url in db:
    channel_data = db[url]['scan_data']['stdout']

    # Use a custom name if set
    if channel_data.get('custom_name'):
        name = channel_data['custom_name']
    else:
        if channel_data.get('programs') is None or \
           channel_data['programs'][0].get('tags') is None or \
           channel_data['programs'][0]['tags'].get('service_name') is None:
            print(
                'Name data not found for "' + url + '".',
                file=sys.stderr
            )
            name = 'Unknown'
        else:
            name = re.sub(
                r'[^\x20-\x7E]+',
                '',
                channel_data['programs'][0]['tags']['service_name']
            )

    # Print playlist entry
    print('    <track>')
    print('        <title>' + name + '</title>')
    print('        <location>' + url + '</location>')
    print('    </track>')

# Print playlist footer
print('  </trackList>')
print('</playlist>')
