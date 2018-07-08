import subprocess
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
        start_time = time()

        try:
            probe_returncode, probe_stdout, probe_stderr = probe.run()
            with self.lock:
                self.addresses[probe.url] = {
                    'returncode': probe_returncode,
                    'stdout': probe_stdout,
                    'stderr': probe_stderr
            }
            if self.debug:
                print('Probe took: ' + str(start_time - time()))
                if probe_returncode:
                    print('Exit code: ' + probe_returncode)
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
