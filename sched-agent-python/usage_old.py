from kubernetes import client, config
from getgpu import gpu_capacity,gpu_used
from getcpu import cpu_capacity,cpu_used
from getmemory import memory_capacity,memory_used
from createpods import pods
from getnodes import getnodes

def main(name='test3',image='nginx',req_cpu=1, req_gpu=1, req_mem=1024, req_nodes=1):

    config.load_kube_config(config_file='./config')
    api_instance = client.CoreV1Api()   
    node_list = api_instance.list_node()
    pod_details = {'name':name,'image':image,'cpus':req_cpu,'gpus':req_gpu,'memory':req_mem}    
    resources={}
    resourcesNodes={}
    selectedZone="None"
    selectedNode="None"


    for node in node_list.items:
      if("master"!=node.metadata.labels["zone"]):
        NODE=node.metadata.name
        #print("Capacity = ",capacity_cpu)
        capacity_cpu=cpu_capacity(NODE)
        used_cpu=cpu_used(NODE)
        avail_cpu=int((capacity_cpu - used_cpu)/1000)
        #print("Used = ",avail_cpu)
        
        capacity_memory=node.status.capacity['memory']
        capacity_memory=(int(capacity_memory[:-2])/1000)
        #capacity_memory=memory_capacity(NODE)
        used_memory=memory_used(NODE)
        avail_memory=int(capacity_memory-used_memory)
        #print("Avail CPUs = ",avail_cpu,"\tAvail Memory = ",avail_memory)

        if("hardware-type" in node.metadata.labels):
          #rint("length ",len(node.status.capacity))
          gpu_position = len(node.status.capacity)
          capacity_gpu=int(node.status.capacity['nvidia.com/gpu'])
          #rint("Capacity ", capacity_gpu)
          used_gpu=int(gpu_used(NODE,str(gpu_position)))
          #pacity_gpu=int(gpu_capacity(NODE))
          #sed_gpu=int(gpu_used(NODE, "7"))
          avail_gpu=capacity_gpu-used_gpu
          #print("Avail GPUs = ", avail_gpu)
        else:
          avail_gpu=0
        
        #if(avail_cpu >= req_cpu and avail_memory >= req_mem and avail_gpu >= req_gpu):
        #  print("Resources Available")

        #else:
        #  print("Not Avilable")
        if(not resources and avail_cpu >= req_cpu and avail_memory >= req_mem and avail_gpu >= req_gpu):
          resources[node.metadata.labels["zone"]]=[{"totalResources": {"avail_cpus":avail_cpu, "avail_memory":avail_memory, "avail_gpus":avail_gpu}}]
          resourcesNodes[node.metadata.labels["zone"]]=[{"node_name":NODE, "avail_cpus":avail_cpu, "avail_memory":avail_memory, "avail_gpus":avail_gpu}]

        else:
          check=0
          for zones in resources:
            if(zones == node.metadata.labels["zone"] and avail_cpu >= req_cpu and avail_memory >= req_mem and avail_gpu >= req_gpu):
              resourcesNodes[zones].append({"node_name":NODE,"avail_cpus":avail_cpu, "avail_memory":avail_memory, "avail_gpus":avail_gpu})
              avail_cpu=avail_cpu+resources[zones][0]["totalResources"]["avail_cpus"]
              avail_gpu=avail_gpu+resources[zones][0]["totalResources"]["avail_gpus"]
              avail_memory=avail_memory+resources[zones][0]["totalResources"]["avail_memory"]
              resources[zones]=[{"totalResources": {"avail_cpus":avail_cpu, "avail_memory":avail_memory, "avail_gpus":avail_gpu}}]
              
             
              check=1
          if(check == 0 and avail_cpu >= req_cpu and avail_memory >= req_mem and avail_gpu >= req_gpu):
            resources[node.metadata.labels["zone"]]=[{"totalResources": {"avail_cpus":avail_cpu, "avail_memory":avail_memory, "avail_gpus":avail_gpu}}]
            resourcesNodes[node.metadata.labels["zone"]]=[{"node_name":NODE,"avail_cpus":avail_cpu, "avail_memory":avail_memory, "avail_gpus":avail_gpu}]

      #print("Total Resources = ",resources)
      #print("Resources in Nodes = ",resourcesNodes)

    #selectedZone=getzone(resources, req_cpu, req_gpu, req_mem, cpu_weight, gpu_weight, mem_weight)    
    if(req_nodes>1):
      print("Required greater than one node")
      #selectedNode={"Zone":selectedZone,"Nodes":selectedNode}
    elif(len(resourcesNodes)>0):
      print(resourcesNodes)
      selectedNode=getnodes(resourcesNodes) #selectedZone, resourcesNodes, req_cpu, req_gpu, req_mem, cpu_weight, gpu_weight, mem_weight)   
      print(selectedNode)
      resp=pods(selectedNode,pod_details)
      print(resp)
    else:
      print(selectedNode)

if __name__ == '__main__':
    main()
