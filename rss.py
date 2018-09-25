import hashlib
import json
import logging
import os
import sys

import feedparser

logger = logging.getLogger('rss')
default_handler = logging.StreamHandler(sys.stdout)
default_handler.setFormatter(logging.Formatter(
    '[%(asctime)s %(name)s] %(levelname)s: %(message)s'))
logger.addHandler(default_handler)
logger.setLevel(logging.DEBUG)


class rss():
    def __init__(self):

        self.urldict = []
        try:
            with open(os.path.split(os.path.realpath(__file__))[0] + '/db.json') as f:
                self.thread = json.load(f)
                logger.debug("Loaded DB. Not first run.")
            self.__init_mark = False
        except:
            self.thread = []
            logger.info("Initialized DB. First run detected!")
            self.__init_mark = True

    def query(self, urldict):
        value = []
        for i, target in enumerate(urldict):
            logger.debug("Querying %s", target)
            post = self.process(urldict[i])
            value.extend(post)
        return value

    def parse(self, url):
        pop = feedparser.parse(url)
        if hasattr(pop, 'bozo_exception'):
            logger.error("Boom at %s", pop.bozo_exception)
        else:
            return pop

    def process(self, url):
        value = []
        pop = self.parse(url)

        for i, post in enumerate(pop.entries):
            hash = hashlib.md5(post.link.encode('utf-8')).hexdigest()
            if hash not in self.thread:
                self.thread.append(hash)
                logger.debug("Getting %s# post at %s", i, url)
                value.append(post)
            else:
                logger.debug("Skipping %s# post at %s", i, url)

        with open('./db.json', 'w+') as f:
            json.dump(self.thread, f)
            logger.debug("Stored DB")
        if self.__init_mark:
            return []

        return value


if __name__ == "__main__":
    URLS = [
        "https://www.cnbeta.com/backend.php",
        "https://www.ithome.com/rss/"
    ]
    r = rss().query(URLS)
    print(r)
