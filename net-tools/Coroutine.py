# coding:utf-8

from greenlet import greenlet

global q
q = ''

def produce(con):
    global q
    if len(q) < 7:
        q += str(len(q))
        q += str(len(q))
    elif len(q) == 7:
        q += str(len(q))
    print q
#    con = greenlet(consumer)
    con.switch(self)

def consumer():
    global q
    if len(q):
        q = q[:len(q) - 1]
    print q
#    pro = greenlet(produce)
    pro.switch(self)

if __name__ == '__main__':
    pro = greenlet(produce)
    con = greenlet(consumer)
    pro.switch(con)