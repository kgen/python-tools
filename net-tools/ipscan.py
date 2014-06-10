import gevent.monkey
from gevent.queue import Queue, Empty
gevent.monkey.patch_socket()

import socket
import gevent
import time

activeips = []
threads = []
tasks = Queue()

def openiptest(name):
    try:
        while True:
            ip = tasks.get(timeout=1)
            #print name,' testing ip: ',ip
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.settimeout(3.0)
            no = c.connect_ex((ip, ))
            if not no:
                print ip
                activeips.append(ip)
                print '--------------------------------',len(activeips)
            c.close()
    except Empty:
        print name,' is quitting!'

def assignip():
    for i in range(1, 2):
        for j in range(1, 255):
#            print 'assigning ip 192.168.' + str(i) + '.' + str(j)
            tasks.put('10.12.' +  '0.'  + str(j))
    print 'assign over!'

for i in xrange(1, 100):
    threads.append(gevent.spawn(openiptest, i))

assignip()
gevent.joinall(threads)
for a in activeips:
    print a
