
import socket
from datetime import datetime, timedelta
import sys
domain_dict = {}
time_dict = {}
ns_array = [] #all ns and the time of update

def Ask_Main_Server(data,parentIP, parentPort):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(data, (parentIP, parentPort))
    data, addr = s.recvfrom(1024)
    s.close()
    return data

def split_zone_line(line):
    parts=line.strip().split(',')
    domain, ip, type = parts
    domain_parts={'domain': domain, 'ip':ip, 'type':type}
    return domain_parts


def Init_Current_Server(myPort, parentIP, parentPort ,x):
    My_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    My_socket.bind(('', myPort))
    while True:
        print("lisening")
        data, addr = My_socket.recvfrom(1024)
        time_domain = time_dict.get(data)
        print("get data")
        now = datetime.now()
        if not time_domain:
            for value in domain_dict.values():
                pass

        if time_domain and time_domain >= now-timedelta(seconds=x): # if domain exist at cache
            print("get data from cache")
            send_data = domain_dict[data]
        else:
            if time_domain:
                print("cache time out reload data")
            else:
                print("Not appear at cache")
            send_data = Ask_Main_Server(data,parentIP, parentPort)
            domain_dict[data] = send_data
            time_dict[data] = now

        split_data = split_zone_line(send_data.decode())

        while split_data['type']=='NS':
            newip ,newport = split_data['ip'].split(':')
            send_data = Ask_Main_Server(data,newip , newport)
            domain_dict[data] = send_data
            time_dict[data] = now
            split_data = split_zone_line(send_data.decode())

        My_socket.sendto(send_data, addr)





if __name__ == "__main__":
    myPort = int(sys.argv[1])
    parentIP = sys.argv[2]
    parentPort = int(sys.argv[3])
    x = int(sys.argv[4])
    Init_Current_Server(myPort, parentIP, parentPort, x)
