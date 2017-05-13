path = "/home/pi/projects/twitterFeed"

import tornado.ioloop
import tornado.web
import signal

application = tornado.web.Application([
    (r'/feed.jpeg()', tornado.web.StaticFileHandler, {'path': path + '/feed.jpeg'}),
])


    
if True:
    application.listen(90)
    tornado.ioloop.IOLoop.instance().start()
