from threading import Thread
from subprocess import Popen, PIPE
from json import loads

class Probe():
    def __init__(self, media_location, debug=False):
        self.result = {}
        self.media_location = media_location
        self.debug = debug

    def run(self, timeout=10):
        probe_thread = Thread(
            target = self.run_ffprobe,
            name = 'probe_thread - ' + self.media_location
        )
        probe_thread.start()
        probe_thread.join(timeout)
        if probe_thread.is_alive():
            self.process.terminate()
            if self.debug: print 'Timeout exceeded: ' + self.media_location
        else:
            return self.result

    def run_ffprobe(self):
        analyze_command = ['ffprobe', '-hide_banner', '-show_programs',
                          '-show_streams', '-print_format', 'json', 
                          # These might help sometimes (?)
                          # '-fflags', 'discardcorrupt',
                          # '-err_detect', 'ignore_err',
                          # '-resync_size', '2147483647',
                          # '-max_ts_probe', '2147483647',
                          self.media_location]

        self.process = Popen(analyze_command, stdout=PIPE, stderr=PIPE)
        self.process.wait()
        analyze_command_output, analyze_command_errors = \
            self.process.communicate()
        exitcode = self.process.returncode

        if exitcode:
            if self.debug:
                print 'ffprobe exited with code: ' + str(exitcode) + \
                    ', location: ' + self.media_location + \
                    ', error: ' + str(analyze_command_errors)
        else:
            try:
                analyze_object = loads(analyze_command_output)
            except ValueError:
                if self.debug:
                    print 'Failure when parsing JSON, location: ' + \
                        self.media_location
                return
            try:
                # Channel name
                self.result['name'] = \
                    analyze_object['programs'][0]['tags']['service_name']
                # Audio track and subtitle languages
                for stream in analyze_object['programs'][0]['streams']:
                    if stream.get('tags') and stream['tags']['language']:
                        stream_type = stream['codec_type']
                        language = stream['tags']['language']
                        if not self.result.get(stream_type):
                            self.result[stream_type] = []
                        self.result[stream_type].append(language)
                # Stream location
                self.result['location'] = self.media_location
            except:
                if self.debug:
                    print 'Failure to find data, location: ' + \
                        self.media_location
