from urllib import request

counts = dict()

fhand = request.urlopen('http://www.py4inf.com/code/romeo.txt')

for line in fhand:
    words = line.split()
    for word in words:
        counts[word.decode()] = counts.get(word.decode(), 0)+1

print(counts)