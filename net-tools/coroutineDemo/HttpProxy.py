#coding: utf-8
import gevent
import urllib2
import simplejson as json
import gevent.monkey
gevent.monkey.patch_socket()

def fetch(pid):
    try:
        response = urllib2.urlopen('http://json-time.appspot.com/time.json')
        result = response.read()
        json_result = json.loads(result)
        datetime = json_result['datetime']

        print('Process %s: %s' % (pid, datetime))
        return json_result['datetime']
    except urllib2.HTTPError, ex:
        print('Process %s: HTTPError: %s' % (pid, ex.msg))

def synchronous():
    for i in range(1, 10):
        fetch(i)

def asynchronous():
    threads = []
    for i in range(1,10):
        threads.append(gevent.spawn(fetch, i))
    gevent.joinall(threads)

if __name__ == '__main__':
    # 代理服务器
    proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    print('Synchronous:')
    synchronous()

    print('Asynchronous:')
    asynchronous()
