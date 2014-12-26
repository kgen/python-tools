import urllib

if __name__ == '__main__':
    url = "http://www.auib.com.cn/product/common/easyQueryVer3/EasyQueryXML.jsp"
    params = urllib.urlencode({'strSql': 'Select * from all_users',
                               'strStart': 1,
                               'LargeFlag': 0,
                               'LimitFlag': 0})
    f = urllib.urlopen(url, params)
    print f.read()