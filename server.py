#!/usr/bin/python27

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
from tornado.options import define, options

import time
import multiprocessing
import arduino

define("port", default=8080, help="run on the given port", type=int)

clients = []

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        clients.append(self)
        self.write_message("connected")

    def on_message(self, message):
        print 'tornado received from client: %s' % message
        self.write_message('got it!')
        q = self.application.settings.get('queue')
        q.put(message)

    def on_close(self):
        print 'connection closed'
        clients.remove(self)

################################ MAIN ################################

def main():

    taskQ = multiprocessing.Queue()
    resultQ = multiprocessing.Queue()

    ard = arduino.Arduino(taskQ, resultQ)
    ard.daemon = True
    ard.start()

    taskQ.put("first task")

    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/ws", WebSocketHandler)
        ], queue=taskQ
    )
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print "Listening on port:", options.port
    #tornado.ioloop.IOLoop.instance().start()
    
    def checkResults():
        if not resultQ.empty():
            result = resultQ.get()
            print "tornado received from arduino: " + result
            for c in clients:
                c.write_message(result)
        
    mainLoop = tornado.ioloop.IOLoop.instance()
    scheduler = tornado.ioloop.PeriodicCallback(checkResults, 10, io_loop = mainLoop)
    scheduler.start()
    mainLoop.start()

if __name__ == "__main__":
    main()

    
