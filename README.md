Usage
=

This is a tool to scan lists of URLs (to anything that the ffprobe from the ffmpeg suite supports - http, ftp, rtsp, udp, etc)

This is the help that's also available from the command itself:

```
usage: run_survey.py [-h] [-f FILE] [-p PATTERNS [PATTERNS ...]]
                     [-c CONCURRENCY] [-t TIMEOUT] [-v VERBOSITY]

Scan URLs for MPEG stream information

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Filename where scan data is persisted
  -p PATTERNS [PATTERNS ...], --patterns PATTERNS [PATTERNS ...]
                        Pattern(s) to scan
  -c CONCURRENCY, --concurrency CONCURRENCY
                        How many probes to run in parallel
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout for a single probe
  -v VERBOSITY, --verbosity VERBOSITY
                        How much information to display during the scan
```
                        
A utility to generate XSPF or M3U playlists is also provided.

Here is the usage of the utility:

```
usage: generate_playlist.py [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                            [-f {xspf,m3u}]

Generate a playlist from JSON data

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        Filename where JSON data is read from
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Filename to write playlist to
  -f {xspf,m3u}, --format {xspf,m3u}
                        Which format to output the playlist in
```
