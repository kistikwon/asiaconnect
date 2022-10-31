from kubernetes import client, config
import json
import random


def getnodes(resourcesNodes):    #selectedZone, resourcesNodes, req_cpu, req_gpu, req_mem, cpu_weight, gpu_weight, mem_weight):

    #node_weight=0.0
    selectedNode="None"
    nodeMaxLen = 0
    selectedZone="None"
    for zones,data in resourcesNodes.items():

      if(len(data)>nodeMaxLen):
        nodeMaxLen = len(data)
        selectedZone = zones
    

      #if(zones == selectedZone):
      #  node_weight=0.0
        
      #  for t in data:

      #    if(t["avail_cpus"]>=req_cpu and t["avail_gpus"]>=req_gpu and t["avail_memory"]>=req_mem):

      #      if(((t["avail_cpus"]*cpu_weight)+(t["avail_gpus"]*gpu_weight)+(t["avail_memory"]*mem_weight))>node_weight):
      #        node_weight=(t["avail_cpus"]*cpu_weight)+(t["avail_gpus"]*gpu_weight)+(t["avail_memory"]*mem_weight)
      #        selectedNode = t["node_name"]

    
    #values = list(range(nodeMaxLen))  
    #selectedNode = resourcesNodes[selectedZone][random.choice(values)]['node_name']
    nd_array = []
    for nodes in resourcesNodes[selectedZone]:
        nd_array.append(nodes['node_name'])

    return nd_array

