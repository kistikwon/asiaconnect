import requests
import json
import sys
import re
import operator

ip = sys.argv[1]

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

szone = 'A'
dzone = 'B'

loss = {}
for i in range(nodeinzone):
    for j in range(nodeinzone):
        if i<j:
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Loss+Tests+-+Loss/203.250.172."+str(i+1)+"/203.250.172."+str(j+1)+"/Packet+Loss/"
            data = transdata(url)
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Loss+Tests+-+Loss/203.250.172."+str(i+1)+"/203.250.172."+str(j+1)+"/Packet+Loss/"
            data2 = transdata(url)
            if data >= data2 and 1-data > 0 :
                score = 100*(1-data*loweight)
            elif data < data2 and 1-data2 > 0 :                
                score = 100*(1-data2*loweight)
            else:
                score = 0
            print("Zone-"+szone+"-"+str(i+1)+", Zone-"+dzone+"-"+str(j+1)+"  Loss :"+str(data))
            print("Zone-"+szone+"-"+str(j+1)+", Zone-"+dzone+"-"+str(i+1)+"  Loss :"+str(data2)+" , score :"+str(score))
            loss[szone+str(i+1)+dzone+str(j+1)] = score
            loss[szone+str(j+1)+dzone+str(i+1)] = score

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
            print("Zone-"+szone+"-"+str(i+1)+", Zone-"+dzone+"-"+str(j+1)+"  Delay :"+str(data))
            print("Zone-"+szone+"-"+str(j+1)+", Zone-"+dzone+"-"+str(i+1)+"  Delay :"+str(data2)+" , score :"+str(score))
            delay[szone+str(i+1)+dzone+str(j+1)] = score
            delay[szone+str(j+1)+dzone+str(i+1)] = score

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
            print("Zone-"+szone+"-"+str(i+1)+", Zone-"+dzone+"-"+str(j+1)+"  Throughput :"+str(data))
            print("Zone-"+szone+"-"+str(j+1)+", Zone-"+dzone+"-"+str(i+1)+"  Throughput :"+str(data2)+" , score :"+str(score))
            throughput[szone+str(i+1)+dzone+str(j+1)] = score
            throughput[szone+str(j+1)+dzone+str(i+1)] = score

total = {}
for i in range(nodeinzone):
    for j in range(nodeinzone):
        if i!=j:
            if (szone+str(i+1)) in total :
                total[szone+str(i+1)] = total[szone+str(i+1)]+loss[szone+str(i+1)+dzone+str(j+1)]+throughput[szone+str(i+1)+dzone+str(j+1)]+delay[szone+str(i+1)+dzone+str(j+1)]
            else : 
                total[szone+str(i+1)] = loss[szone+str(i+1)+dzone+str(j+1)]+throughput[szone+str(i+1)+dzone+str(j+1)]+delay[szone+str(i+1)+dzone+str(j+1)]

print(total)
total2 = sorted(total.items(), key=operator.itemgetter(1), reverse=True)
print(total2)

#filternode = max(total,key=total.get)
#print("Filter node: "+filternode+", max score is : "+str(max(total.values())))
