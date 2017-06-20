#!/usr/bin/env python3
import re
import os
import sys
import urllib.request
import json


class Thread(object):
    def __init__(self, url):
        self.url = url
        self.board, self.threadno = self._to_elements(url)
        self._response = None

    @property
    def images(self):
        images = []
        base_image_url = "http://images.4chan.org/{}/src/".format(self.board)

        for post in self.json['posts']:
            if 'ext' in post:
                filename = "{}{}".format(post['tim'], post['ext'])
                url = base_image_url + filename
                images.append( (filename, url) )
        return images

    @property
    def json(self):
        if self._response:
            return self._response

        url = "http://api.4chan.org/{}/res/{}.json".format(
            self.board, self.threadno)
        response = json.loads(urllib.request.urlopen(url).readall().decode('utf-8'))

        self._response = response
        return response

    @property
    def dirname(self):
        return "{}_{}".format(self.board, self.threadno)

    def _to_elements(self, url):
        try:
            board, threadno = re.search(r'(\w+)/res/(\d+)', url).groups()
        except AttributeError:
            raise ValueError("Invalid url!")
        return board, int(threadno)


def main(url):
    t = Thread(url)

    try:
        os.makedirs(t.dirname)
    except OSError:
        pass
    os.chdir(t.dirname)

    for filename, url in t.images:
        if not os.path.exists(filename):
            try:
                with open(filename, 'wb') as f:
                    f.write(urllib.request.urlopen(url).readall())
            except HTTPError:
                os.unlink(filename)
            print("Done '{}'.".format(url))


if __name__ == "__main__":
    main(sys.argv[1])