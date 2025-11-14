import socket
import sys
ip=sys.argv[1]
port=int(sys.argv[2])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    print("insert input:")
    data = input()
    s.sendto(data.encode(), (ip, port))
    data, addr = s.recvfrom(1024)
    print(str(data.decode()))
s.close()