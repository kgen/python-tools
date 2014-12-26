import signal

def handler(signum, _):
    if  signum == signal.SIGINT:
        print "sigint"
    elif signum == signal.SIGABRT:
        print "sigABRT"
    else:
        print signum

def main():
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGABRT, handler)
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGBREAK, handler)
    signal.signal(signal.SIGILL, handler)
    sign = raw_input("signal:")
    while sign != "exit":
         sign = raw_input("signal:")

if __name__ == '__main__':
    main()