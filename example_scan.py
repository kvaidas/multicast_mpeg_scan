from multicast_mpeg_scan.scan import Scan
import json

probe_list = []
for ip in range(1,255):
    probe_list.append( 'http://stream_ip_part.' + str(ip) + ':1234' )

scanner = Scan(probe_list, timeout=10, concurrency=4)
result = scanner.run()

result_file=open('results_json.txt','w')
json.dump(result, result_file, indent=4)
