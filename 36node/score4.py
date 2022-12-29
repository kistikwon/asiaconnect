import requests
import json
import sys
import re
import operator

ip = sys.argv[1]
neednode = sys.argv[2]

thweight = 1
loweight = 100
deweight = 1
nodeinzone = 9

def transdata(url):
    data = requests.get(url)
    binary = data.content
    output = json.loads(binary)
    r = output['message']
    regex = re.compile('[^0-9.]')
    return float(regex.sub('',r))

p=ip.split('.')
n = int(p[3])
if n >= 1 and n < 10:
    zone = 1
elif n >=10 and n < 19:
    zone = 2
elif n >=18 and n < 28:
    zone = 3
elif n >= 28 and n < 37:
    zone = 4


loss = {}
delay = {}
throughput = {}
total = {}
iplist = []
selectlist = []
pretotal = {}

for j in range(int(neednode)):
    iplist.append(n)
    for i in range(nodeinzone):
        zoneip = 9*(zone-1)+i+1
        if zoneip not in iplist:
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Loss+Tests+-+Loss/"+ip+"/203.250.172."+str(zoneip)+"/Packet+Loss/"
            data = transdata(url)
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Loss+Tests+-+Loss/203.250.172."+str(zoneip)+"/"+ip+"/Packet+Loss/"
            data2 = transdata(url)
            if data >= data2 and 20-data*loweight > 0 :
                score = 20-data*loweight
            elif data < data2 and 20-data2*loweight > 0 :
                score = 20-data2*loweight
            else:
                score = 0
            print(ip+", 203.250.172."+str(zoneip)+"  Loss :"+str(data))
            print("203.250.172."+str(zoneip)+", "+ip+"  Loss :"+str(data2)+" , score :"+str(score))
            loss[str(ip)+"203.250.172."+str(zoneip)] = score
            loss["203.250.172."+str(zoneip)+str(ip)] = score

    for i in range(nodeinzone):
        zoneip = 9*(zone-1)+i+1
        if zoneip not in iplist:
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Delay+Tests+-+Delay/"+ip+"/203.250.172."+str(zoneip)+"/Delay/"
            data = transdata(url)
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Delay+Tests+-+Delay/203.250.172."+str(zoneip)+"/"+ip+"/Delay/"
            data2 = transdata(url)
            if data >= data2 and 40-deweight*data > 0 :
                score = 40-deweight*data
            elif data < data2 and 40-deweight*data2 > 0:
                score = 40-deweight*data2
            else:
                score = 0
            print(ip+", 203.250.172."+str(zoneip)+"  Delay :"+str(data))
            print("203.250.172."+str(zoneip)+", "+ip+"  Delay :"+str(data2)+" , score :"+str(score))
            delay[str(ip)+"203.250.172."+str(zoneip)] = score
            delay["203.250.172."+str(zoneip)+str(ip)] = score

    for i in range(nodeinzone):
        zoneip = 9*(zone-1)+i+1
        if zoneip not in iplist:
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Throughput+Tests+-+Throughput/"+ip+"/203.250.172."+str(zoneip)+"/Throughput/"
            data = transdata(url)
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Throughput+Tests+-+Throughput/203.250.172."+str(zoneip)+"/"+ip+"/Throughput/"
            data2 = transdata(url)
            if data >= data2 :
                score = 40*data2*thweight
            elif data < data2 :
                score = 40*data*thweight
            print(ip+", 203.250.172."+str(zoneip)+"  Throughput :"+str(data))
            print("203.250.172."+str(zoneip)+", "+ip+"  Throughput :"+str(data2)+" , score :"+str(score))
            throughput[str(ip)+"203.250.172."+str(zoneip)] = score
            throughput["203.250.172."+str(zoneip)+str(ip)] = score

    for i in range(nodeinzone):
        zoneip = 9*(zone-1)+i+1
        if zoneip not in iplist:
            if "203.250.172."+str(zoneip) in pretotal :
                total["203.250.172."+str(zoneip)] =  pretotal["203.250.172."+str(zoneip)] + loss[str(ip)+"203.250.172."+str(zoneip)]+throughput[str(ip)+"203.250.172."+str(zoneip)]+delay[str(ip)+"203.250.172."+str(zoneip)]
            else :
                total["203.250.172."+str(zoneip)] = loss[str(ip)+"203.250.172."+str(zoneip)]+throughput[str(ip)+"203.250.172."+str(zoneip)]+delay[str(ip)+"203.250.172."+str(zoneip)]

    total2 = sorted(total.items(), key=operator.itemgetter(1), reverse=True)
    pretotal = dict(total2)
    print(total2)
    print("======================="+str(total2[0][0])+"=========================")
    ip = str(total2[0][0])
    p=ip.split('.')
    n = int(p[3])
    selectlist.append(ip)
    total = {}
print(selectlist)