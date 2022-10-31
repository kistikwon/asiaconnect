from kubernetes import client, config
import json


def getzone(resources, req_cpu, req_gpu, req_mem, cpu_weight, gpu_weight, mem_weight):
  selectedZone="None"
  total_weight=0.0
  for zones in resources:
    if(resources[zones][0]["totalResources"]["avail_cpus"]>=req_cpu and resources[zones][0]["totalResources"]["avail_gpus"]>=req_gpu and resources[zones][0]["totalResources"]["avail_memory"]>=req_mem):
      if(((resources[zones][0]["totalResources"]["avail_cpus"]*cpu_weight)+(resources[zones][0]["totalResources"]["avail_gpus"]*gpu_weight)+(resources[zones][0]["totalResources"]["avail_memory"]*mem_weight))>total_weight):
        total_weight=(resources[zones][0]["totalResources"]["avail_cpus"]*cpu_weight)+(resources[zones][0]["totalResources"]["avail_gpus"]*gpu_weight)+(resources[zones][0]["totalResources"]["avail_memory"]*mem_weight)
        selectedZone=zones
  return selectedZone
