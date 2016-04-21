from urllib import request

fhand = request.urlopen('http://www.py4inf.com/code/romeo.txt')

for line in fhand:
    print(line.strip().decode())
