import json, requests
import re

url = 'http://134.75.115.137/maddash/grids/APRP+Measurements+-+Example+Throughput+Tests+-+Throughput/Parkistan121.52.154.6/KistiTest203.250.172.1/Throughput/'
url1 = 'https://perfsonar.nrp-nautilus.io/maddash/grids/Nautilus+Mesh+-+Latency+a2a+-+OWDelay/us-central+i2-houston/us-central+i2-kansas/One-way+Delay'

params = dict(
    throughput='message',
)

data = requests.get(url)
#print(data.json())
binary = data.content
output = json.loads(binary)
r = output['message']
regex = re.compile('[^0-9.]')
print(float(regex.sub('',r)))
#print(''.join(filter(lambda x: x.isdigit(), r)))

# test to see if the request was valid
#print output['status']

# output all of the results
#pprint.pprint(output)

# step-by-step directions
