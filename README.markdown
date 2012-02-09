# rand\_imgur

## A script to download random images from imgur

### Requirements
- [lxml](http://lxml.de/)
- [requests](http://docs.python-requests.org/en/latest/index.html)
- [twisted](http://twistedmatrix.com/trac/)

### Usage
    -h, --help        : display help message
    -f, --folder      : folder to download images to, default = images/
    -i, --interval    : interval between requests (seconds), default = 1
    -l, --log         : send logging output to rand\_imgur.log, not stdout
    -s, --sendheaders : send Firefox http headers
