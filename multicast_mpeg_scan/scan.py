import subprocess
import sys
from json import loads
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from multicast_mpeg_scan.probe import Probe


class Scan:
    def __init__(self, concurrency=4, timeout=30, verbose=False):
        self.addresses = {}
        self.__executor = ThreadPoolExecutor(max_workers=concurrency)
        self.timeout = timeout
        self.verbose = verbose
        self.lock = Lock()

    def add(self, url):
        self.addresses[url] = None

    def __run_probe(self, probe):

        try:
            probe_returncode, probe_stdout, probe_stderr = probe.run()
            with self.lock:
                self.addresses[probe.media_location] = {
                    'returncode': probe_returncode,
                    'stdout': loads(probe_stdout),
                    'stderr': probe_stderr
                }

        except subprocess.TimeoutExpired as exception:
            if self.verbose:
                print(exception, file=sys.stderr)
        except Exception as exception:
            print(exception)

    def run(self):
        for url in self.addresses:
            self.__executor.submit(
                self.__run_probe,
                Probe(url, timeout=self.timeout, verbose=self.verbose)
            )
        self.__executor.shutdown(wait=True)

        return self.addresses
