
import socket
from datetime import datetime, timedelta
import sys
domain_dict = {}
time_dict = {}
ns_dict={}

#This func checks if the data contains existing ns that at the cache
def check_if_in_ns(data,x):
    now = datetime.now()
    for domain in ns_dict.keys():
        if data.decode().endswith(domain):
            if ns_dict[domain][1] >= now - timedelta(seconds=x):
                send_data = ns_dict[domain][0]
                return send_data
    return None

#This func ask server for the result
def ask_main_server(data, parent_ip, parent_port):
    # print("ask main server ip "+str(parent_ip)+" port "+str(parent_port))
    now = datetime.now()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(data, (parent_ip, parent_port))
    data_rec, addr = s.recvfrom(1024)
    s.close()
    domain_dict[data] = data_rec
    time_dict[data] = now
    return data_rec

#This func split the result for information
def split_zone_line(line):
    parts=line.strip().split(',')
    domain, ip, type = parts
    domain_parts={'domain': domain, 'ip':ip, 'type':type}
    return domain_parts

#This func is the main func
def init_current_server(my_port, parent_ip, parent_port, x):
    #open socket
    my_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.bind(('', my_port))
    while True:
        is_updated = False
        # print("listening")
        data, addr = my_socket.recvfrom(1024)
        time_domain = time_dict.get(data)
        # print("get data")
        now = datetime.now()
        send_data = None
        #if the data already at cache
        if time_domain and time_domain >= now-timedelta(seconds=x): # if domain exist at cache
            # print("get data from cache")
            send_data = domain_dict[data]
        else:
            #if it at the cache but timeout
            if time_domain:
                pass
                # print("cache time out reload data")
            else:
                #if it not at cache so check if it at the ns cache
                # print("check if it at ns cache")
                send_data = check_if_in_ns(data,x)
            #if it no where ask the main server
            if send_data is None:
                # print("Not appear at cache")
                send_data = ask_main_server(data, parent_ip, parent_port)
                is_updated = True

        # update ns dict and make the ns chain
        # print(send_data)
        if send_data.decode().strip() != 'non-existent domain':
            split_data = split_zone_line(send_data.decode())
            if is_updated and split_data["type"] == 'NS':
                ns_dict[split_data["domain"]] = [send_data, now]
            while split_data['type']=='NS':
                newip ,newport = split_data['ip'].split(':')
                send_data = ask_main_server(data, newip , int(newport))
                if send_data.decode().strip() == 'non-existent domain':
                    break
                split_data = split_zone_line(send_data.decode())

        my_socket.sendto(send_data, addr)





if __name__ == "__main__":
    myPort = int(sys.argv[1])
    parentIP = sys.argv[2]
    parentPort = int(sys.argv[3])
    x = int(sys.argv[4])
    init_current_server(myPort, parentIP, parentPort, x)
