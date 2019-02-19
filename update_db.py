import json
import sys
from datetime import datetime
from multicast_mpeg_scan.scan import Scan

# Build URL list
urls = []
for ip in range(0, 255):
    urls.append('udp://224.0.0.' + str(ip) + ':1234')

# Run the scan
scanner = Scan(concurrency=4, timeout=30, verbose=True)
for url in urls:
    scanner.add(url)
scan_results = scanner.run()

# Read the channel database
try:
    with open('channel_db.json', mode='r') as db_file:
        db = json.load(db_file)
except FileNotFoundError:
    db = {}

# Update channel data
for url in urls:
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
with open('channel_db.json', mode='w') as db_file:
    json.dump(
        db,
        db_file,
        indent=4
    )
