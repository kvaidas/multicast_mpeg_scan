import subprocess
import sys
from time import time


class Probe:
    def __init__(self, media_location, timeout=30, verbosity=1):
        self.media_location = media_location
        self.timeout = timeout
        self.verbosity = verbosity

    def run(self):
        analyze_command = [
            'ffprobe', '-hide_banner',
            '-show_programs',
            '-show_streams',
            '-print_format', 'json',
            '-show_error',
            self.media_location
        ]

        if self.verbosity >= 2:
            print(
                'Starting probe for "' + self.media_location + '".',
                file=sys.stderr
            )
        start_time = time()
        probe_process = subprocess.run(
            analyze_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=self.timeout,
            bufsize=1048576
        )
        if self.verbosity >= 2:
            probe_time = round(time() - start_time, 3)
            print(
                'Ended probe for "' + self.media_location +
                '" in ' + str(probe_time) + 's. Exit code: ' + str(probe_process.returncode),
                file=sys.stderr
            )
            if probe_process.returncode:
                print(
                    'stdout: ' + probe_process.stdout.decode('utf-8'),
                    file=sys.stderr
                )
                print(
                    'stderr: ' + probe_process.stderr.decode('utf-8'),
                    file=sys.stderr
                )

        return (
            probe_process.returncode,
            probe_process.stdout.decode('utf-8'),
            probe_process.stderr.decode('utf-8')
        )
