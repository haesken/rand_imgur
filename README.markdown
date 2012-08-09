# rand\_imgur

A script to download random images from imgur

## Requirements
- [requests](http://docs.python-requests.org/en/latest/index.html)
- [twisted](http://twistedmatrix.com/trac/)

## Usage

    python rand_imgur.py [options]

## Options
    -h, --help        : display help message
    -f, --folder      : folder to download images to, default = images/
    -i, --interval    : interval between requests (seconds), default = 1
    -l, --log         : send logging output to rand\_imgur.log, not stdout
