import subprocess
from json import loads
from threading import Lock
from time import time
from concurrent.futures import ThreadPoolExecutor
from multicast_mpeg_scan.probe import Probe


class Scan:
    def __init__(self, concurrency=4, timeout=30):
        self.addresses = {}

        self.concurrency = concurrency
        self.timeout = timeout
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
                    'time': round(time() - start_time, 3)
                }

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
                Probe(url, timeout=self.timeout)
            )
        executor.shutdown(wait=True)

        return self.addresses
