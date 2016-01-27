from Queue import Queue
from threading import Semaphore, Thread
from multicast_mpeg_scan.probe import Probe

class Scan():
    def __init__(self, stream_locations, concurrency=5, timeout=10, debug=False):
        self.stream_queue = Queue()
        self.results = Queue()

        self.concurrency = concurrency
        self.running_threads = Semaphore(self.concurrency)
        self.timeout = timeout
        self.debug = debug

        for stream_location in stream_locations:
            self.stream_queue.put(stream_location)
        if self.debug:
            print "Imported " + str(self.stream_queue.qsize()) + " items."

    def run(self):
        probe_threads = []
        while self.stream_queue.qsize() > 0:
            self.running_threads.acquire()
            location = self.stream_queue.get()
            probe_thread = Thread(
                target = self.run_probe,
                args = (location,),
                name = 'scan_thread - ' + location
            )
            probe_thread.start()
            probe_threads.append(probe_thread)
        for probe_thread in probe_threads:
            probe_thread.join()

        channel_list = []
        while self.results.qsize() > 0:
            channel_list.append(self.results.get())
        return channel_list

    def run_probe(self, location):
        probe = Probe(location, debug=self.debug)
        program = probe.run(self.timeout)
        if program:
            self.results.put(program)
            if self.debug: print "Found: " + str(program)
        elif self.debug:
            print "Program name not found for: " + location
        self.running_threads.release()
