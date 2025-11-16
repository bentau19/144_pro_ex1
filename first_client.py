#first part- the client sends the student's names to the server's specific IP and port
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b'Ben Tau and Yael Doron', ('192.168.253.123', 12346))
data, addr = s.recvfrom(1024)
print(str(data), addr)
s.close()