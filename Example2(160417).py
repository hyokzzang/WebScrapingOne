import socket
import time

# Type of socket and address
#   AF_INET : Address type which if IPv4 (AF_INET6 : IPv6)
#   SOCK_STREAM : Data transmission type (consistent than SOCK_DGRAM)
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the socket
mysock.connect(('www.py4inf.com', 80))

# Encode the message : These lines should be added in the case of Python 3
message = 'GET http://www.py4inf.com/cover.jpg HTTP/1.0\n\n')
message = message.encode('utf-8')

# Send the message to the end of socket
mysock.send(message)

count = 0
picture = "";
while True:
    data = mysock.recv(5120)
    if( len(data) < 1) : break
    
    # time.sleep(0.25)
    count = count + len(data)
    print len(data), count
    picture = picture + data


