import subprocess


class Probe:
    def __init__(self, media_location, timeout=30, debug=False):
        self.media_location = media_location
        self.timeout = timeout
        self.debug = debug

    def run(self):
        analyze_command = [
            'ffprobe', '-hide_banner', '-show_programs',
            '-show_streams', '-print_format', 'json', '-show_error',
            '-read_intervals', '%+' + str(self.timeout-5),
            '-timeout', '5',
            self.media_location
        ]

        probe_process = subprocess.run(
            analyze_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=self.timeout,
            bufsize=1048576
        )

        return (
            probe_process.returncode,
            probe_process.stdout.decode('utf-8'),
            probe_process.stderr.decode('utf-8')
        )
