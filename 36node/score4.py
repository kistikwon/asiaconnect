import requests
import json
import sys
import re
import operator

ip = sys.argv[1]
neednode = sys.argv[2]

thweight = 1
loweight = 1
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
for i in range(nodeinzone):
    zoneip = 9*(zone-1)+i
    if zoneip != n:
        url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Loss+Tests+-+Loss/"+ip+"/203.250.172."+zoneip+"/Packet+Loss/"
        data = transdata(url)
        url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Loss+Tests+-+Loss/203.250.172."+zoneip+"/"+ip+"/Packet+Loss/"
        data2 = transdata(url)
        if data >= data2 and 1-data > 0 :
            score = 100*(1-data*loweight)
        elif data < data2 and 1-data2 > 0 :                
            score = 100*(1-data2*loweight)
        else:
            score = 0
        print(ip+", 203.250.172."+zoneip+"  Loss :"+str(data))
        print("203.250.172."+zoneip+", "+ip+"  Loss :"+str(data2)+" , score :"+str(score))
        loss[str(ip)+"203.250.172."+str(zoneip)] = score
        loss["203.250.172."++str(i+1)] = score



delay = {}
for i in range(nodeinzone):
    for j in range(nodeinzone):
        if i<j:            
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Delay+Tests+-+Delay/203.250.172."+str(i+1)+"/203.250.172."+str(j+1)+"/Delay/"
            data = transdata(url)
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Delay+Tests+-+Delay/203.250.172."+str(i+1)+"/203.250.172."+str(j+1)+"/Delay/"
            data2 = transdata(url)
            if data >= data2 :
                score = 100-deweight*data
            elif data < data2 :
                score = 100-deweight*data2
            print("203.250.172."+str(i+1)+", 203.250.172."+str(j+1)+"  Delay :"+str(data))
            print("203.250.172."+str(j+1)+", 203.250.172."+str(i+1)+"  Delay :"+str(data2)+" , score :"+str(score))
            delay[str(i+1)+str(j+1)] = score
            delay[str(j+1)+str(i+1)] = score

throughput = {}
for i in range(nodeinzone):
    for j in range(nodeinzone):
        if i<j:
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Throughput+Tests+-+Throughput/203.250.172."+str(i+1)+"/203.250.172."+str(j+1)+"/Throughput/"
            data = transdata(url)
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Throughput+Tests+-+Throughput/203.250.172."+str(i+1)+"/203.250.172."+str(j+1)+"/Throughput/"
            data2 = transdata(url)
            if data >= data2 :
                score = 100*data2*thweight
            elif data < data2 :
                score = 100*data*thweight
            print("203.250.172."+str(i+1)+", 203.250.172."+str(j+1)+"  Throughput :"+str(data))
            print("203.250.172."+str(j+1)+", 203.250.172."+str(i+1)+"  Throughput :"+str(data2)+" , score :"+str(score))
            throughput[str(i+1)+str(j+1)] = score
            throughput[str(j+1)+str(i+1)] = score

total = {}
for i in range(nodeinzone):
    for j in range(nodeinzone):
        if i!=j:
            if (str(i+1)) in total :
                total[str(i+1)] = total[str(i+1)]+loss[str(i+1)+str(j+1)]+throughput[str(i+1)+str(j+1)]+delay[str(i+1)+str(j+1)]
            else : 
                total[str(i+1)] = loss[str(i+1)+str(j+1)]+throughput[str(i+1)+str(j+1)]+delay[str(i+1)+str(j+1)]

total2 = sorted(total.items(), key=operator.itemgetter(1), reverse=True)
print(total2)
print(type(total))
print(type(total2))
for i in range(int(neednode)):
    print("203.250.172."+str(total2[i][0]))
