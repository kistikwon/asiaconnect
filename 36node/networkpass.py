import requests
import json
import sys
import re
import operator

def networkpass(argv)
    thweight = 1
    loweight = 100
    deweight = 1

    ip = argv[1]
    neednode = int(argv[len(argv)-1])-1
    nodeinzone = len(argv)-2

    urldelay = 'http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Delay+Tests+-+Delay'
    urlloss = 'http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Loss+Tests+-+Loss'
    urlth = 'http://134.75.115.137/maddash/grids/36Node+Measurements+-+Example+Throughput+Tests+-+Throughput'

    datadelay = requests.get(urldelay)
    dataloss = requests.get(urlloss)
    datath = requests.get(urlth)
    binarydelay = datadelay.content
    binaryloss = dataloss.content
    binaryth = datath.content
    outputdelay = json.loads(binarydelay)
    outputloss = json.loads(binaryloss)
    outputth = json.loads(binaryth)
    delayoutput = outputdelay['grid']
    lossoutput = outputloss['grid']
    throughputoutput = outputth['grid']
    regex = re.compile('[^0-9.]')

    p=ip.split('.')
    n = int(p[3])


    loss = {}
    delay = {}
    throughput = {}
    total = {}
    iplist = []
    selectlist = []
    pretotal = {}

    selectlist.append(ip)


    for j in range(int(neednode)):
        iplist.append(ip)
        p=ip.split('.')
        n = int(p[3])
        for i in range(nodeinzone):
            if argv[i+1] not in iplist:
                p2 = argv[i+1].split('.')
                n2 = int(p2[3])
                data = float(regex.sub('',lossoutput[n-1][n2-1][0]['message']))
                data2 = float(regex.sub('',lossoutput[n2-1][n-1][0]['message']))
                if data >= data2 and 20-data*loweight > 0 :
                    score = 20-data*loweight
                elif data < data2 and 20-data2*loweight > 0 :
                    score = 20-data2*loweight
                else:
                    score = 0
                print(ip+" , "+argv[i+1]+"  Loss :"+str(data))
                print(argv[i+1]+" , "+ip+"  Loss :"+str(data2)+" , score :"+str(score))
                loss[ip+","+argv[i+1]] = score
                loss[argv[i+1]+","+ip] = score

        for i in range(nodeinzone):
            if argv[i+1] not in iplist:
                p2 = argv[i+1].split('.')
                n2 = int(p2[3])
                data = float(regex.sub('',delayoutput[n-1][n2-1][0]['message']))
                data2 = float(regex.sub('',delayoutput[n2-1][n-1][0]['message']))
                if data >= data2 and 40-deweight*data > 0 :
                    score = 40-deweight*data
                elif data < data2 and 40-deweight*data2 > 0:
                    score = 40-deweight*data2
                else:
                    score = 0
                print(ip+" , "+argv[i+1]+"  Delay :"+str(data))
                print(argv[i+1]+" , "+ip+"  Delay :"+str(data2)+" , score :"+str(score))
                delay[ip+","+argv[i+1]] = score
                delay[argv[i+1]+","+ip] = score

        for i in range(nodeinzone):
            if argv[i+1] not in iplist:
                p2 = argv[i+1].split('.')
                n2 = int(p2[3])
                data = float(regex.sub('',throughputoutput[n-1][n2-1][0]['message']))
                data2 = float(regex.sub('',throughputoutput[n2-1][n-1][0]['message']))
                if data >= data2 :
                    score = 40*data2*thweight
                elif data < data2 :
                    score = 40*data*thweight
                print(ip+" , "+argv[i+1]+"  Throughput :"+str(data))
                print(argv[i+1]+" , "+ip+"  Throughput :"+str(data2)+" , score :"+str(score))
                throughput[ip+","+argv[i+1]] = score
                throughput[argv[i+1]+","+ip] = score

        for i in range(nodeinzone):
            if argv[i+1] not in iplist:
                if argv[i+1] in pretotal :
                    total[argv[i+1]] =  pretotal[argv[i+1]] + loss[ip+","+argv[i+1]]+throughput[ip+","+argv[i+1]]+delay[ip+","+argv[i+1]]
                else :
                    total[argv[i+1]] = loss[ip+","+str(argv[i+1])]+throughput[ip+","+str(argv[i+1])]+delay[ip+","+str(argv[i+1])]

        total2 = sorted(total.items(), key=operator.itemgetter(1), reverse=True)
        pretotal = dict(total2)
        print(total2)
        print("======================= Node Select : "+str(total2[0][0])+"=========================")
        ip = str(total2[0][0])
        selectlist.append(ip)
        total = {}

    print(selectlist)

return(selectlist)