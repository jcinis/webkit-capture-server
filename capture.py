#!/usr/bin/env python
#
# Copyright 2010 Polychrome
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import time, os, random

define("port", default=80, help="run on the given port", type=int)

ROOT_DIR = os.path.split(os.path.split(__file__)[0])[0]

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("You probably shouldn't be here.")

class UrlHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/urlform.html")

    def post(self):
        #self.set_header("Content-Type", "text/plain")
        #self.write("Fetching URL:" + self.get_argument('url'))

        url = self.get_argument('url')
        # check url here
        filepath = '%s/screenshots/%s-%s' % (time.time(),random.randint(0,999999999))
        #command = '%s/webkit2png.py --width=1200 --height=1000 --fullsize --delay=2 --filename=%s %s' % (filepath,url)
        command = '%s/webkit2png.py --width=990 --height=620 --fullsize --delay=3 --filename=%s %s' % (ROOT_DIR, filepath, url)
        os.system(command)
        filepath = '%s-full.png' % filepath
        if os.path.exists(filepath):
            self.set_header("Content-Type","image/png")
            with open(filepath,'rb') as f:
                self.write(f.read())
            if os.path.isfile(filepath):
                os.unlink(filepath)

def main():
    cache_path = '/private/var/root/Library/Caches/org.python.python.app/Cache.db'
    if os.path.exists(cache_path):
        os.unlink(cache_path)

    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/url", UrlHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
