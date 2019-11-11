#!/usr/bin/env python3

import json
import re
import sys
import argparse
import datetime

# Parse cli arguments
arg_parser = argparse.ArgumentParser(
    description='Generate a playlist from JSON data'
)
arg_parser.add_argument(
    '-i', '--input-file',
    help='Filename where JSON data is read from'
)
arg_parser.add_argument(
    '-o', '--output-file',
    help='Filename to write playlist to'
)
arg_parser.add_argument(
    '-f', '--format',
    choices=['xspf', 'm3u'],
    default='xspf',
    help='Which format to output the playlist in'
)
arg_parser.add_argument(
    '-d', '--days',
    type=int,
    help='Ignore channels last seen more than days specified'
)
arguments = arg_parser.parse_args()

# Date filtering setup
age_threshold = None
if arguments.days:
    age_delta = datetime.timedelta(days=arguments.days)
    age_threshold = datetime.datetime.now() - age_delta

# Load stream information
db = {}
if arguments.input_file:
    with open(arguments.input_file) as db_file:
        db = json.load(db_file)
else:
    print('Warning: using stdin as input', file=sys.stderr)
    db = json.load(sys.stdin)

# Setup the output
if arguments.output_file:
    playlist_file = open(arguments.output_file, 'w')
else:
    playlist_file = sys.stdout

#
# Print the playlist
#

# Print playlist header
if arguments.format == 'xspf':
    print('<?xml version="1.0" encoding="UTF-8"?>', file=playlist_file)
    print('<playlist version="1" xmlns="http://xspf.org/ns/0/">', file=playlist_file)
    print('  <trackList>', file=playlist_file)
elif arguments.format == 'm3u':
    print('#EXTM3U', file=playlist_file)

# Iterate over available channels
for url in db:
    # Skip channel if it is too old
    updated_date = datetime.datetime.strptime(
        db[url]['last_updated'],
        '%Y-%m-%d %H:%M:%S'
    )
    if age_threshold is not None and updated_date < age_threshold:
        print(db[url], file=sys.stderr)
        continue

    channel_data = db[url]['scan_data']['stdout']

    # Use a custom name if set
    if channel_data.get('custom_name'):
        name = channel_data['custom_name']
    else:
        if channel_data.get('programs') is None or \
           len(channel_data['programs']) == 0 or \
           channel_data['programs'][0].get('tags') is None or \
           channel_data['programs'][0]['tags'].get('service_name') is None:
            print(
                'Data not found for "' + url + '".',
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
    if arguments.format == 'xspf':
        print('    <track>', file=playlist_file)
        print('        <title>' + name + '</title>', file=playlist_file)
        print('        <location>' + url + '</location>', file=playlist_file)
        print('    </track>', file=playlist_file)
    elif arguments.format == 'm3u':
        print('#EXTINF:-1,' + name, file=playlist_file)
        print(url, file=playlist_file)

# Print playlist footer
if arguments.format == 'xspf':
    print('  </trackList>', file=playlist_file)
    print('</playlist>', file=playlist_file)
