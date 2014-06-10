import socket
import re
def resolve_google_iplist(google_hosts):
        resolved_iplist = []
        need_resolve_remote = []
        for host in google_hosts:
            if re.match(r'\d+\.\d+\.\d+\.\d+', host):
                resolved_iplist += [host]
                continue
            try:
                iplist = socket.gethostbyname_ex(host)[-1]
                if len(iplist) >= 2:
                    resolved_iplist += iplist
                else:
                    need_resolve_remote += [host]
            except (socket.error, OSError):
                need_resolve_remote += [host]
        if len(resolved_iplist) < 32 or len(set(x.split('.', 1)[0] for x in resolved_iplist)) == 1:
            print 'local google_hosts=%s is too short, try remote_resolve' % google_hosts
            need_resolve_remote += [x for x in google_hosts if not re.match(r'\d+\.\d+\.\d+\.\d+', x)]

        print resolved_iplist
        print need_resolve_remote

hostlist = ['203.208.48.148', '203.208.48.144', '203.208.48.145', '203.208.48.146', '203.208.48.147']
resolve_google_iplist(hostlist)