import nmap
nm = nmap.PortScanner()

def getNetDeviceCount():
    nm.scan(hosts='192.168.1.0/24',arguments='-n -sP -PE -PA21,23,80,3389')
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    for host, status in hosts_list:
        print('{0}:{1}'.format(host, status))
    print ('count ' + str(len(hosts_list)))
    return str(len(hosts_list))