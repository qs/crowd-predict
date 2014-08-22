from datetime import datetime
import json
from urlparse import urlparse
from pymongo.connection import Connection
from bson import json_util
import socket

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

MONGO_URL = "mongodb://heroku:BKDdotDH_0viI8yJR86uH8kfJ_IV6hfywNc8fvg1tu5C_aCnPvA2aw-7iqvIEZKCBka2MPAposp8S0-GYApp_Q@kahana.mongohq.com:10006/app28781290"

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/add", AddHandler)
        ]

        settings = dict(
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        if socket.gethostname() != 'note':
            self.con = Connection(MONGO_URL)
            self.database = self.con[urlparse(MONGO_URL).path[1:]]
        else:
            self.con = Connection('localhost', 27017)
            self.database = self.con["crowdpred"]


class MainHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.database

    def get(self):
        entries = self.db["entries"].find()
        j_entries = []
        if entries:
            for entry in entries:
                j_entry = json.dumps(entry, default=json_util.default)
                j_entries.append(j_entry)
            self.write( json.dumps(j_entries) )

class AddHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.database

    def get(self):
        entry = self.get_argument("entry", None)
        author = self.get_argument("author", None)
        if entry and author:
            new_comment = {
                "entry" : entry,
                "author" : author,
                "time" : datetime.utcnow(),
            }

            self.db.entries.insert(new_comment)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()