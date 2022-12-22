import requests
import json
import sys
import re

szone = sys.argv[1]
dzone = sys.argv[1]

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

loss = {}
for i in range(nodeinzone):
    for j in range(nodeinzone):
        if i!=j:
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Loss+Tests+-+Loss/Zone-"+szone+"-"+str(i+1)+"/Zone-"+dzone+"-"+str(j+1)+"/Packet+Loss/"
            data = transdata(url)
            if 1-data > 0:
                score = 100*(1-data*loweight)
            else:
                score = 0
            print("Zone-"+szone+"-"+str(i+1)+", Zone-"+dzone+"-"+str(j+1)+"  Loss :"+str(data)+" , score :"+str(score))
            loss[szone+str(i+1)+dzone+str(j+1)] = score
		
print(loss)

throughput = {}
for i in range(nodeinzone):
    for j in range(nodeinzone):
        if i!=j:
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Throughput+Tests+-+Throughput/Zone-"+szone+"-"+str(i+1)+"/Zone-"+dzone+"-"+str(j+1)+"/Throughput/"
	    data = transdata(url)
	    score = 100*data*trweight
	    print("Zone-"+szone+"-"+str(i+1)+", Zone-"+dzone+"-"+str(j+1)+"  Throughput :"+str(data)+" , score :"+str(score))
	    throughput[szone+str(i+1)+dzone+str(j+1)] = score

print(throughput)

trace = {}
total = {}
for i in range(nodeinzone):
    for j in range(nodeinzone):
        if i!=j:
            url = "http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Traceroute+Tests+-+Path+Count/Zone-"+szone+"-"+str(i+1)+"/Zone-"+dzone+"-"+str(j+1)+"/Traceroute+Path+Count/"
	    data = transdata(url)
	    score = 100*thweight*1/data
	    print("Zone-"+szone+"-"+str(i+1)+", Zone-"+dzone+"-"+str(j+1)+"  Trace :"+str(data)+" , score :"+str(score))
	    trace[szone+str(i+1)+dzone+str(j+1)] = score
	    total[szone+str(i+1)+dzone+str(j+1)] = loss[szone+str(i+1)+dzone+str(j+1)]+throughput[szone+str(i+1)+dzone+str(j+1)]+trace[szone+str(i+1)+dzone+str(j+1)]

print(total)

filternode = max(total,key=total.get)
print("Filter node: "+filternode+", max score is : "+str(max(total.values())))
