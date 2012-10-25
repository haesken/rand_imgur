# rand\_imgur

A script to download random images from imgur

## Requirements
- [requests](http://docs.python-requests.org/en/latest/index.html)
- [twisted](http://twistedmatrix.com/trac/)
- [docopt](http://github.com/docopt/docopt)

## Usage

    rand_imgur.py [options]

## Options

    -h --help           Show this help
    -d --directory DIR  Directory to download images to [default: images]
    -i --interval N     Seconds between each request [default: 1]
    -l --log            Write output to a log instead of stdout
