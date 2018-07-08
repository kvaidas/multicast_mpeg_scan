import subprocess


class Probe:
    def __init__(self, media_location, timeout=30, debug=False):
        self.result = {}
        self.media_location = media_location
        self.timeout = timeout
        self.debug = debug
        self.process = None
        self.error = None

    def run(self):
        analyze_command = [
            'ffprobe', '-hide_banner', '-show_programs',
            '-show_streams', '-print_format', 'json', '-show_error',
            '-read_intervals', '%+' + str(self.timeout-5),
            '-timeout', '5',
            self.media_location
        ]

        self.process = subprocess.run(
            analyze_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=self.timeout,
            bufsize=1048576
        )

        return (
            self.process.returncode,
            self.process.stdout.decode('utf-8'),
            self.process.stderr.decode('utf-8')
            )
