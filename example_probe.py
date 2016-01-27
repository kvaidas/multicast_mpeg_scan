from multicast_mpeg_scan.probe import Probe

probe = Probe('http://stream_url')
probe_result = probe.run(10)

if probe_result:
    print probe_result
else:
    print "Probe unsuccessful."
