from getnodes import getnodes
from networkpass import networkpass

    resources={}
    resourcesNodes={203.250.172.1,203.250.172.2,203.250.172.3}
    selectedZone="None"
    selectedNode="None"

    selectedNode=getnodes(resourcesNodes)
    print(selectedNode)
