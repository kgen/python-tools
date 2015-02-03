import gevent
from gevent.queue import Queue
from gevent.queue import Empty

tasks = Queue()

def worker(n):
    while not tasks.empty():
        task = tasks.get()
        print('Worker %s got task %s' % (n, task))
        gevent.sleep(0)

    print('Quitting time!')

def boss():
    for i in xrange(1, 25):
        tasks.put_nowait(i)

tasks1 = Queue(maxsize=3)

def worker1(n):
    try:
        while True:
            task1 = tasks1.get(timeout=1)  # decrements queue size by 1
            print('Worker %s got task %s' % (n, task1))
            gevent.sleep(0)
    except Empty:
        print('Quitting time!')

def boss1():
    """
    Boss will wait to hand out work until a individual worker is
    free since the maxsize of the task queue is 3.
    """

    for i in xrange(1, 10):
        tasks1.put(i)
    print('Assigned all work in iteration 1')

    for i in xrange(10, 20):
        tasks1.put(i)
    print('Assigned all work in iteration 2')

def main():
    gevent.spawn(boss).join()

    gevent.joinall([
        gevent.spawn(worker, 'steve'),
        gevent.spawn(worker, 'john'),
        gevent.spawn(worker, 'nancy'),
    ])

    gevent.joinall([
        gevent.spawn(boss1),
        gevent.spawn(worker1, 'steve1'),
        gevent.spawn(worker1, 'john1'),
        gevent.spawn(worker1, 'bob1'),
    ])

if __name__ == '__main__':
    main()
