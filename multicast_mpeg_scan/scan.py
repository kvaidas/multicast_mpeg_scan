import subprocess
from json import loads
from threading import Lock
from time import time
from concurrent.futures import ThreadPoolExecutor
from multicast_mpeg_scan.probe import Probe


class Scan:
    def __init__(self, concurrency=4, timeout=30, debug=False):
        self.addresses = {}

        self.concurrency = concurrency
        self.timeout = timeout
        self.debug = debug
        self.lock = Lock()

    def add(self, url):
        self.addresses[url] = None

    def __run_probe(self, probe):

        try:
            start_time = time()
            probe_returncode, probe_stdout, probe_stderr = probe.run()
            with self.lock:
                self.addresses[probe.media_location] = {
                    'returncode': probe_returncode,
                    'stdout': loads(probe_stdout),
                    'stderr': probe_stderr,
                    'time': time() - start_time
                }
            if self.debug:
                if probe_returncode:
                    print('Probe failed. Exit code: ' + probe_returncode)
                    print('stdout: ' + probe_stdout)
                    print('stderr: ' + probe_stderr)

        except subprocess.TimeoutExpired as exception:
            print(exception)
        except ValueError as exception:
            print(exception)
        except Exception as exception:
            print(exception)

    def run(self):
        executor = ThreadPoolExecutor(max_workers=self.concurrency)
        for url in self.addresses:
            executor.submit(
                self.__run_probe,
                Probe(url, timeout=self.timeout, debug=self.debug)
            )
        executor.shutdown(wait=True)

        return self.addresses
