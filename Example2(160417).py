import socket
import time
import base64
import codecs

# Type of socket and address
#   AF_INET : Address type which if IPv4 (AF_INET6 : IPv6)
#   SOCK_STREAM : Data transmission type (consistent than SOCK_DGRAM)
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the socket
mysock.connect(('www.py4inf.com', 80))

# Encode the message : These lines should be added in the case of Python 3
message = 'GET http://www.py4inf.com/cover.jpg HTTP/1.0\n\n'
message = message.encode('utf-8')

# Send the message to the end of socket
mysock.send(message)

count = 0
picture = "";
#picture = codecs.encode(picture)
while True:
    data = mysock.recv(5120)
    
    if( len(data) < 1) : break
    
    # time.sleep(0.25)
    count = count + len(data)
    print(len(data), count)
    picture = picture + data.decode('cp437')
    #picture = picture + data

mysock.close()

# Look for the end of the header (2 CRLF)
pos = picture.find("\r\n\r\n")
print('Header length', pos)
print(picture[:pos])

# Skip past the header and save the picture data
picture = picture[pos+4:]
#picture = picture.encode('base64')
picture = codecs.encode(picture)
#picture = picture.decode('base64')
#imgdata = base64.b64decode(picture)
fhand = open("stuff.jpg", "wb")
fhand.write(picture);
fhand.close()

