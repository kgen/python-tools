import gevent.monkey
from gevent.queue import Queue, Empty
gevent.monkey.patch_socket()

import socket
import gevent

activeips = []
threads = []
tasks = Queue()


def openiptest(name):
    try:
        while True:
            ip = tasks.get(timeout=1)
            print name,' testing ip: ',ip    
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.settimeout(3.0)
            no = c.connect_ex(ip)
            if not no:
                print ip
                activeips.append(ip)
                print '--------------------------------',len(activeips)	
            c.close()
    except Empty:
        print name,' is quitting!'


def AssignIPAndPort():
    for i in range(168, 169):
        for j in range(1, 255):
            for k in range(80, 81):
                tasks.put(('192.' + str(i) + '.1.' + str(j), k))
    print 'assign over!'

def AssignPort():
    for k in range(10, 10000):
        tasks.put(('218.75.86.238', k))
    print 'assign over!'

for i in xrange(100, 150):
    threads.append(gevent.spawn(openiptest, i))

AssignIPAndPort()
#AssignPort()
#ipta = tasks.get(timeout=1)
#print ipta
gevent.joinall(threads)
for a in activeips:
    print a
