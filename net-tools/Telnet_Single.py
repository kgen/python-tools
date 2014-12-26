import telnetlib
import time

server = '192.168.1.254'
user = 'root'
value = 'admin1'


def dotest():
    try:
        print 'begin'
        tn = telnetlib.Telnet(server)
        tn.read_until("login: ", 4)
        tn.write(user + "\n")
        tn.read_until("Password: ")
        tn.write(value + "\n")
        result = tn.read_very_eager()
        while len(result) <= 2:
            result = tn.read_very_eager()
        print result, value
        if 'incorrect' not in result:
            print "Login successful:", value, user
        tn.close()
    except Exception, ex:
        print ex.message

dotest()