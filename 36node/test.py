import requests
import json
import sys
import re
import operator


url = 'http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Delay+Tests+-+Delay'
data = requests.get(url)
binary = data.content
output = json.loads(binary)
r = output['grid']
print(r[1][5])
k = r[1][5][0]['message']
regex = re.compile('[^0-9.]')
print(float(regex.sub('',k)))
print(type(r))
print(type(k))
print(k)




'''
ip = sys.argv[1]
neednode = sys.argv[len(sys.argv)-1]
#neednode = sys.argv[2]
print("neednode : " + neednode)
print(sys.argv)
print(type(sys.argv))
print("hello"+ip)
print(type(ip))
print(ip[3])


print(ip)
print(ip.split('.'))
p=ip.split('.')
print(p[3])
print(type(p[3]))
a = [1 ,2 ,3 ,4]
if int(p[3]) not in a :
    print('xx')


zoneip = 9
url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Loss+Tests+-+Loss/"+ip+"/203.250.172."+str(zoneip)+"/Packet+Loss/"
print(url)

def add_para(*args):
    print(args)
    return sum(args)

add_para(3,4,5,6), add_para(1,2,3,4,5,6,7,8,9,10)
'''