#!/usr/bin/env python

""" Grab random images from imgur """

import argparse
import md5
import os
import requests
import sys
from random import choice
from string import letters, digits
from time import strftime, sleep
from twisted.python import log


def get_args(): #{{{
    """ Get arguments from the command line. """

    parser = argparse.ArgumentParser(
            description="Grab random images from imgur",
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-f", "--folder", type=str, default="images/",
            help="Optional name of the folder to download images to.\n" +
                "Must include a slash at the end of the path.\n" +
                "Default is 'images/'")

    # Don't be evil, keep the interval at a sane speed
    parser.add_argument("-i", "--interval", type=float, default=1,
            help="Interval between requests (seconds), default = 1")

    parser.add_argument("-l", "--log", action="store_true",
            help="Output to log file instead of the terminal")

    parser.add_argument("-s", "--sendheaders", action="store_true",
            help="Send Firefox HTTP headers")

    args = parser.parse_args()
    return args #}}}


def gen_url(): #{{{
    """ Generate an imgur url using random characters.
        Returns the full url and the short imgur name.
    """

    base = "http://www.imgur.com/"
    imgur_name = "".join([choice(letters + digits) for _ in range(5)])
    extension = ".jpg"

    url = base + imgur_name + extension

    return (url, imgur_name) #}}}


def grab_url(url, use_headers): #{{{
    """ Grab a url, return the content, headers, and status code of the
        response.
        Has a toggle to send Firefox http headers.
    """

    # Firefox http headers {{{
    headers_firefox = {
            "User-Agent": ("User-Agent: Mozilla/5.0 "
                           "(Windows NT 6.1; WOW64; rv:10.0) "
                           "Gecko/20100101 Firefox/10.0"),
            "Accept": ("text/html,application/xhtml+xml,"
                       "application/xml;q=0.9,*/*;q=0.8"),
            "Accept-Language": "en-us,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            } #}}}

    try:
        # Toggle to send Firefox http headers
        if use_headers == True:
            req = requests.get(url, headers=headers_firefox)
        else:
            req = requests.get(url)

        return (req.status_code, req.headers, req.content)

    # Ignore connection errors
    except requests.exceptions.ConnectionError:
        pass #}}}


def is_404_gif(image): #{{{
    """ Check if an image is imgur's 404 gif. """

    hash_404_gif = "eebc93350a68a64022b7482f460017ba"
    hash_image = md5.new(image).hexdigest()

    if hash_image == hash_404_gif:
        return True #}}}


def write_image(filename, image, dirpath): #{{{
    """ Write the image to a file. """

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    outputfile = open(dirpath + filename, "w")
    outputfile.write(image)
    outputfile.close() #}}}


def grab_image(dirpath, use_headers): #{{{
    """ Grab a random image from imgur and write it to a file. """

    (url, imgur_name) = gen_url()
    (response_status, response_headers, image) = grab_url(url, use_headers)

    content_type_header = response_headers["content-type"]
    image_content_types = ["image/gif", "image/jpeg", "image/png"]

    # Keep this status code check here so we don't crash on a bad response
    if response_status == 200:
        if content_type_header in image_content_types:
            if not is_404_gif(image):
                timestamp = strftime("%F %H-%M-%S")
                extension = content_type_header[6:]

                log.msg("Found: www.imgur.com/%s.%s" % (imgur_name, extension))

                filename = "%s %s.%s" % (timestamp, imgur_name, extension)
                log.msg("Writing: %s" % filename)

                write_image(filename, image, dirpath) #}}}


def main(): #{{{
    """ Run forever, grab an image every N seconds. """

    try:
        args = get_args()

        if args.log == True:
            log_filename = "rand_imgur.log"
            log.startLogging(open(log_filename, "a"))
        else:
            log.startLogging(sys.stdout)

        while True:
            grab_image(args.folder, args.sendheaders)
            sleep(args.interval)

    except KeyboardInterrupt:
        sys.exit() #}}}


if __name__ == '__main__':
    main()