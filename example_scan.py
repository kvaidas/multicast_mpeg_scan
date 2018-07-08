import json
import sys

from multicast_mpeg_scan.scan import Scan

scanner = Scan(concurrency=1, timeout=30)
for ip in range(1, 255):
    scanner.add('udp://224.0.0.' + str(ip) + ':1234')

scan_results = scanner.run()
json.dump(scan_results, fp=sys.stdout, indent=4)
