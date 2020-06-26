# Web Video Feed
Stream video feed online with Flask

## Optional Arguments
`-v` or `--video` : Video input device (default=0)

`-m` or `--mode` : Video detection mode : 0=none, 1=face, 2=motion (default=0)

`-p` or `--password` : Set a password to protect video stream (default=None)

`-a` or `--min-area` : Minimum detection area (default=500, only works with motion detection mode)

`-r` or `--record` : Record video captured : 0=no, 1=yes (default=0, only works with motion detection mode)
