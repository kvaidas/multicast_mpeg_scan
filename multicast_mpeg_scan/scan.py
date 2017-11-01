from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from re import findall
import sys

from multicast_mpeg_scan.probe import Probe


class Scan:
    def __init__(self, concurrency=4, timeout=10, debug=False):
        self.addresses = []
        self.results = Queue()

        self.concurrency = concurrency
        self.timeout = timeout
        self.debug = debug

    def add(self, url):
        self.addresses.append(url)

    def __get_probe_result(self, probe):
        result = probe.run()
        if result is not None:
            self.results.put(result)
        elif self.debug:
            print(
                'Error probing ' + probe.media_location + ': ' + probe.error,
                file=sys.stderr
            )

    def run(self):
        executor = ThreadPoolExecutor(max_workers=self.concurrency)
        for url in self.addresses:
            probe = Probe(url, timeout=self.timeout, debug=self.debug)
            executor.submit(
                self.__get_probe_result,
                probe
            )
        executor.shutdown(wait=True)

        # Return the gathered results
        scan_result = []
        while not self.results.empty():
            scan_result.append(
                self.results.get()
            )
        scan_result = sorted(
            scan_result,
            key=lambda result: findall('[0-9]+|[^0-9]+', result['location'])
        )
        return scan_result
