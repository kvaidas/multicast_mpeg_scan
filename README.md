Usage
=

Edit example_scan to contain the correct URL pattern and settings (concurrency and timeout)

`python3 example_scan > scan_results.json`

To convert the results to a VLC playlist:

`cat scan_results.json | python3 vlc_playlist.py > playlist.xspf`