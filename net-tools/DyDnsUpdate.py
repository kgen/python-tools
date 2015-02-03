# coding: utf-8
import urllib2
import base64
import time
import re
from HTMLParser import HTMLParser

wanip = ''
wanip_old = ''

http_timeout = 3
ipregex = r'(((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-4]|[01]?\d\d?))'

dydns_domain = '*.f3322.net'
dydns_delay = 120
dydns_username = 'dydns'
dydns_password = 'dydns_pwd'

route_ip = '192.168.1.1'
router_username = 'router'
router_password = 'router_pwd'
router_authtip = '; ChgPwdSubTag='


'''
HTMLParser的成员函数:

    handle_startendtag  处理开始标签和结束标签
    handle_starttag     处理开始标签，比如<xx>
    handle_endtag       处理结束标签，比如</xx>
    handle_charref      处理特殊字符串，就是以&#开头的，一般是内码表示的字符
    handle_entityref    处理一些特殊字符，以&开头的，比如
    handle_data         处理数据，就是<xx>data</xx>中间的那些数据
    handle_comment      处理注释
    handle_decl         处理<!开头的，比如<!DOCTYPE html PUBLIC “-//W3C//DTD HTML 4.01 Transitional//EN”
    handle_pi           处理形如<?instruction>的东西

'''
class myHtmlParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.flag=None

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.flag = 'script'

    def handle_data(self, data):
        if self.flag == 'script' and 'wanPara=new Array' in data:
            self.flag = 'wanip'
            ips = re.findall(ipregex, data)
            if len(ips) > 0:
                ip = ips[0][0]
                print 'Find IP: %s' % ip
                recordWanIP(ip)
            else:
                print 'Not Find IP!'

    def handle_endtag(self, tag):
        if self.flag == 'wanip':
            self.flag = None

def updateDyDnsIP():
    try:
        url = 'http://members.3322.net/dyndns/update' \
          '?hostname=' + dydns_domain + \
          '&myip=' + wanip + \
          '&wildcard=OFF' \
          '&mx=mail.exchanger.ext' \
          '&backmx=NO' \
          '&offline=NO'
        auth = 'Basic ' + base64.b64encode(dydns_username + ':' + dydns_password)
        heads = {'Authorization': auth,
             'User-Agent': 'myclient/1.0 me@null.net'
        }

        # request status html
        request = urllib2.Request(url, None, heads)
        response = urllib2.urlopen(request, timeout=http_timeout)

        result = response.read()
        print 'Update Result:%s' % result
    except urllib2.HTTPError, e:
        print 'Update Request Err:%s' % e.code
    except Exception, e:
        print 'Update Err:%s' % e.message

def getwanIPfromRouter():
    try:
        url = 'http://' + route_ip + '/userRpm/StatusRpm.htm'
        auth = 'Authorization=' + 'Basic%20' + \
               base64.b64encode(router_username + ':' + router_password) + \
               router_authtip
        heads = {'Cookie': auth,
                 'connection': 'keep-alive',
                 'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) "
                               "Chrome/39.0.2171.99 Safari/537.36",
                 'Referer': 'http://192.168.1.1/',
                 'Accept-Encoding': 'gzip, deflate, sdch',
                 'Accept-Language': 'zh-CN,zh;q=0.8'
        }

        # request status html
        request = urllib2.Request(url, None, heads)
        response = urllib2.urlopen(request, timeout=http_timeout)
        content = response.read()

        # parse the html result and find wan ip
        m = myHtmlParser()
        m.feed(content)
        m.close()

    except urllib2.HTTPError, e:
        print 'GetWanIP Request Err:%s' % e.msg
    except Exception, e:
        print 'GetWanIP Err:%s' % e.message

def getWanIPfrom3322Org():
    pass

def recordWanIP(ip):
    global wanip_old, wanip
    wanip_old = wanip
    wanip = ip

def main():
    while True:
        getwanIPfromRouter()
        if wanip != wanip_old:
            updateDyDnsIP()
        else:
            print 'IP no Change!'
        time.sleep(dydns_delay)

if __name__ == '__main__':
    main()


