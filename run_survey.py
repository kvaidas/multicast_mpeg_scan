#!/usr/bin/env python3

import json
import sys
import argparse
from datetime import datetime
from multicast_mpeg_scan.scan import Scan

# Parse cli arguments
arg_parser = argparse.ArgumentParser(
    description='Scan URLs for MPEG stream information'
)
arg_parser.add_argument(
    '-f', '--file',
    help='Filename where scan data is persisted'
)
arg_parser.add_argument(
    '-p', '--patterns',
    nargs='+',
    help='Pattern(s) to scan'
)
arg_parser.add_argument(
    '-c', '--concurrency',
    default=1,
    type=int,
    help='How many probes to run in parallel'
)
arg_parser.add_argument(
    '-t', '--timeout',
    help='Timeout for a single probe'
)
arg_parser.add_argument(
    '-v', '--verbosity',
    default=1,
    help='How much information to display during the scan'
)
arguments = arg_parser.parse_args()

scanner = Scan(
    concurrency = arguments.concurrency,
    timeout = arguments.timeout,
    verbosity = arguments.verbosity
)

# Build URL list from parameters
if arguments.patterns:
    for pattern_spec in arguments.patterns:
        pattern_spec = pattern_spec.split('@')
        pattern = pattern_spec[0]
        iterator = eval(pattern_spec[1])
        for i in iterator:
            scanner.add(
                pattern.format(i)
            )

# Build URL list from stdin
for url in sys.stdin.readlines():
    scanner.add(
        url.strip()
    )

# Run the scan
scan_results = scanner.run()

# Read the channel database
db = {}
if arguments.file:
    try:
        with open(arguments.file, mode='r') as db_file:
            db = json.load(db_file)
    except FileNotFoundError:
        pass

# Update channel data
for url in scanner.addresses.keys():
    # Skip if there is no data for the scan altogether
    if not scan_results[url]:
        print('Error: scan data for "' + url + '" was not present.', file=sys.stderr)
        continue
    # Skip if scan failed
    if scan_results[url]['returncode']:
        continue

    # Skip if the scan didn't have a channel name and no name present in the database
    # Note: doesn't skip if channel not present in database altogether
    try:
        scan_results[url]['stdout']['programs'][0]['tags']['service_name']
    except Exception as ex:
        if db.get(url) and \
           db[url].get('programs') and \
           db[url]['programs'][0].get('tags') and \
           db[url]['programs'][0]['tags']['service_name']:
            continue

    # Create a dict if this URL is new
    if not db.get(url):
        db[url] = {}

    # Update timestamp on channel
    db[url]['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save scan data
    db[url]['scan_data'] = scan_results[url]

# Save channel data to file
if arguments.file:
    db_file = open(arguments.file, mode='w')
else:
    db_file = sys.stdout

json.dump(
    db,
    db_file,
    indent=4
)
