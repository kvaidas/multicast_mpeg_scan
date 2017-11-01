import subprocess
import json
import sys


class Probe:
    def __init__(self, media_location, timeout=10, debug=False):
        self.result = {}
        self.media_location = media_location
        self.timeout = timeout
        self.debug = debug
        self.process = None
        self.error = None

    def run(self):
        if self.debug:
            print(
                'Running probe for: ' + self.media_location,
                file=sys.stderr
            )
        analyze_command = [
            'ffprobe', '-hide_banner', '-show_programs',
            '-show_streams', '-print_format', 'json', '-show_error',
            self.media_location
        ]

        try:
            self.process = subprocess.Popen(
                analyze_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1048576
            )
            self.process.wait(self.timeout)
        except subprocess.TimeoutExpired:
            self.error = 'Timeout exceeded'
            return

        if self.process.returncode:
            self.error = self.process.stderr.read()
            return

        try:
            analyze_object = json.load(self.process.stdout)
        except ValueError:
            self.error = 'Failure parsing JSON'
            return

        # Channel name
        self.result['name'] = \
            analyze_object['programs'][0]['tags']['service_name']

        # Stream metadata
        for stream in analyze_object['programs'][0]['streams']:
            stream_type = stream['codec_type']

            # Video
            if stream_type == 'video':
                self.result['video'] = {
                    'width':  stream['width'],
                    'height': stream['height'],
                    'codec':  stream['codec_name']
                }

            # Audio and subtitles
            if stream.get('tags') and stream['tags']['language']:
                language = stream['tags']['language']
                if not self.result.get(stream_type):
                    self.result[stream_type] = []
                self.result[stream_type].append(
                    {language: stream['codec_name']}
                )

        # Stream location
        self.result['location'] = self.media_location

        return self.result
