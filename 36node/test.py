import requests
import json
import sys
import re
import operator


ip = sys.argv[1]

print("hello"+ip)
print(type(ip))
print(ip[3])


print(ip)
print(ip.split('.'))
p=ip.split('.')
print(p[3])
print(type(p[3]))

if int(p[3]) < 30 :
    print('xx')