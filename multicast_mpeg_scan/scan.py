import subprocess
import sys
import traceback
from datetime import timedelta
from json import loads
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from multicast_mpeg_scan.probe import Probe
from time import time


class Scan:
    def __init__(self, concurrency=4, timeout=30, verbosity=1):
        self.addresses = {}
        self.__executor = ThreadPoolExecutor(max_workers=concurrency)
        self.timeout = timeout
        self.verbosity = verbosity
        self.lock = Lock()

    def add(self, url):
        self.addresses[url] = None

    def __run_probe(self, probe):

        try:
            start_time = time()
            probe_returncode, probe_stdout, probe_stderr = probe.run()
            scan_time = round(time() - start_time, 3)
            with self.lock:
                self.addresses[probe.media_location] = {
                    'returncode': probe_returncode,
                    'stdout': loads(probe_stdout),
                    'stderr': probe_stderr,
                    'scan_time': scan_time
                }
        except subprocess.TimeoutExpired as exception:
            if self.verbosity >= 2:
                print(exception, file=sys.stderr)
            self.addresses[probe.media_location]['stderr'] = 'Process timed out'
        except Exception:
            print(traceback.format_exc())

    def run(self):
        start_time = time()
        for url in self.addresses:
            self.__executor.submit(
                self.__run_probe,
                Probe(url, timeout=self.timeout, verbosity=self.verbosity)
            )
        self.__executor.shutdown(wait=True)
        if self.verbosity >= 1:
            # Count scan time
            scan_time = round(time() - start_time)
            readable_time = timedelta(seconds=scan_time)

            # Count successful probes and URLs with name data
            successful_probes = 0
            named_channels = 0
            for url in self.addresses:
                try:
                    if not self.addresses[url]['returncode']:
                        successful_probes += 1
                except KeyError:
                    pass
                try:
                    self.addresses[url]['stdout']['programs'][0]['tags']['service_name']
                    named_channels += 1
                except KeyError:
                    pass

            print(
                'Scan completed in ' + str(readable_time) + ' URLs: ' + str(len(self.addresses)) +
                ' Successful: ' + str(successful_probes) + ' With namedata: ' + str(named_channels),
                file=sys.stderr
            )

        return self.addresses
