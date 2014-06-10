import socket

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind(('0.0.0.0', 8080))
c.listen(10)

for x in xrange(10):
    temp, addrrrr = c.accept()
    temp.send('hello!')
    print addrrrr
    temp.close()

c.close()