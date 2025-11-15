import socket
import sys

def InnitCurrentServer(port,zone_file):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    while True:
        data, addr = s.recvfrom(1024)
        domain=data.decode().strip()
        ip_of_domain=find_domain_ip(domain,zone_file)
        s.sendto(ip_of_domain.encode(), addr)

def split_zone_line(line):
    parts=line.strip().split(',')
    domain, ip, type = parts
    domain_parts={'domain': domain, 'ip':ip, 'type':type}
    return domain_parts

def find_domain_ip(domain_name,zone_file):
    with open(zone_file, 'r') as file:
        for line in file:
            splited_line=split_zone_line(line)
            if(splited_line['domain']==domain_name or
                    (domain_name.endswith(splited_line['domain'])and
                     splited_line['type']=='NS')):
                return line
    return 'non-existent domain'

if __name__=="__main__":
    port=int(sys.argv[1])
    file=sys.argv[2]
    InnitCurrentServer(port,file)
