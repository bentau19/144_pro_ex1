import socket
import sys

def InnitCurrentServer(port,zone_file):
    # Initialize the current server to listen for queries
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    while True:
        data, addr = s.recvfrom(1024)
        # Decode the domain and strip whitespaces
        domain=data.decode().strip()
        ip_of_domain=find_domain(domain,zone_file)
        s.sendto(ip_of_domain.encode(), addr)

def split_zone_line(line):
    # Split the line by comma and save the parts in a dictionary for easy access
    parts=line.strip().split(',')
    domain, ip, type = parts
    domain_parts={'domain': domain, 'ip':ip, 'type':type}
    return domain_parts

def find_domain(domain_name,zone_file):
    # Function to search for a domain or an ending of a domain (for NS record)
    temp_ns = None
    # Open the zone file for reading
    with open(zone_file, 'r') as file:
        for line in file:
            splited_line=split_zone_line(line)
            # If an exact match is found, return the full line
            if splited_line['domain']==domain_name:
                return line
            # If the domain ends with a domain defined by an NS record, store this NS record
            if (domain_name.endswith(splited_line['domain'])and
                     splited_line['type']=='NS'):
                temp_ns = line
        if temp_ns is not None:
            return temp_ns
    # If no matching A record or NS record was found after checking the entire file return 'non-existent domain'
    return 'non-existent domain'

if __name__=="__main__":
    port=int(sys.argv[1])
    file=sys.argv[2]
    InnitCurrentServer(port,file)
