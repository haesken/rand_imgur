#!/usr/bin/env python
# encoding: utf-8

""" Rand Imgur - Download random images from imgur.

Usage:
  rand_imgur.py [options]

Options:
  -h --help           Show this help
  -d --directory DIR  Directory to download images to [default: images]
  -i --interval N     Seconds between each request [default: 1]
  -l --log            Write output to a log instead of stdout

"""

import md5
import os
import requests
import sys

from docopt import docopt
from random import choice
from string import letters, digits
from time import strftime, sleep
from twisted.python import log


def gen_url():
    """ Generate an imgur url using random characters.
        Returns the full url and the short imgur name.
    """

    base = "http://www.imgur.com/"
    imgur_name = "".join([choice(letters + digits) for _ in range(5)])

    url = base + imgur_name + ".jpg"
    return (url, imgur_name)


def grab_url(url):
    """ Grab a url, return the content, headers, and status code of the
        response.
    """

    try:
        req = requests.get(url)
        return (req.status_code, req.headers, req.content)

    # Ignore connection errors
    except (requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.RequestException):
        pass


def is_404_image(image):
    """ Check if an image is imgur's 404 gif. """

    hash_404_image = "d835884373f4d6c8f24742ceabe74946"
    hash_image = md5.new(image).hexdigest()

    if hash_image == hash_404_image:
        return True


def write_image(filename, image, dirpath):
    """ Write an image to a file. """

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    outputfile = open(os.path.join(dirpath, filename), "w")
    outputfile.write(image)
    outputfile.close()


def grab_image(url, imgur_name, dirpath):
    """ Grab a random image from imgur and write it to a file. """

    response_status, response_headers, image = grab_url(url)

    content_type_header = response_headers["content-type"]
    image_content_types = ["image/gif", "image/jpeg", "image/png"]

    # Keep this status code check here so we don't crash on a bad response
    if response_status == 200:
        if content_type_header in image_content_types:
            if not is_404_image(image):
                timestamp = strftime("%F %H-%M-%S")
                extension = content_type_header[6:]

                log.msg("Found: www.imgur.com/{imgur_name}.{extension}".format(
                    imgur_name=imgur_name, extension=extension))

                filename = "{timestamp} {imgur_name}.{extension}".format(
                        timestamp=timestamp,
                        imgur_name=imgur_name,
                        extension=extension)

                log.msg("Writing: {filename}".format(filename=filename))

                write_image(filename, image, dirpath)


def main(args):
    """ Run forever, grab an image every N seconds. """

    if args["--log"] == True:
        log_filename = "rand_imgur.log"
        log.startLogging(open(log_filename, "a"))
    else:
        log.startLogging(sys.stdout)

    tried_log_path = 'tried.log'
    if os.path.exists(tried_log_path):
        tried_log = open(tried_log_path, "r")
        tried = tried_log.readlines()
        tried_log.close()
    else:
        tried = None

    tried_log = open(tried_log_path, "a+")

    while True:
        url, imgur_name = gen_url()
        if not url in tried:
            grab_image(url, imgur_name, args["--directory"])
            tried.append(url)
            tried_log.write(url + '\n')
        else:
            log.msg("Found {url} in list, not trying.".format(url=url))

        sleep(float(args["--interval"]))


if __name__ == '__main__':
    try:
        main(docopt(__doc__))
    except KeyboardInterrupt:
        sys.exit()
