import time

from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream


def createpods(api_instance,nodes,pods_details):
    name = str(pods_details['name'])
    image = str(pods_details['image'])
    cpu = str(pods_details['cpus'])
    gpu = str(pods_details['gpus'])
    memory = pods_details['memory']
    mem = str(memory)+"Mi"
    #print("GPUs ", gpu)
    #exit(1)
    resp = None
    try:
        resp = api_instance.read_namespaced_pod(name=name,
                                                namespace='default')
    except ApiException as e:
        if e.status != 404:
            #print("Unknown error: %s" % e)
            exit(1)

    if not resp:
        #print("Pod %s does not exist. Creating it..." % name)
        pod_manifest = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'name': name
            },
            'spec': {
                'containers': [{
                    'image': image,
                    'name': 'sleep',
                    "args": [
                        "/bin/sh",
                        "-c",
                        "while true;do date;sleep 5; done"
                    ],
                    "resources": {
                      "requests": {
                        "cpu": cpu,
                        "memory": mem,
                        "nvidia.com/gpu": gpu,
                  },
                      "limits": {
                        "cpu": cpu,
                        "memory": mem,
                        "nvidia.com/gpu": gpu,
                  }

                }
                }],
                "affinity": {
                  "nodeAffinity": {
                    "requiredDuringSchedulingIgnoredDuringExecution": {
                      "nodeSelectorTerms": [
                        {
                           "matchExpressions": [
                             {
                               "key": "kubernetes.io/hostname",
                               "operator": "In",
                               "values": nodes  #["malaysia-node","pakistan-node"]
                          }
                        ]
                      }
                    ]
                  }
                }
              } 
            }
        }
        resp = api_instance.create_namespaced_pod(body=pod_manifest,
                                                  namespace='default')
    return {"status":"pod created"}
        #while True:
        #    resp = api_instance.read_namespaced_pod(name=name, namespace='default')
        #    if resp.status.phase != 'Pending':
        #        break
        #    time.sleep(1)
        #print("Created on Node = ",nodes)
        

def pods(nodes,pods_details):
    config.load_kube_config()
    try:
        c = Configuration().get_default_copy()
    except AttributeError:
        c = Configuration()
        c.assert_hostname = False
    Configuration.set_default(c)
    core_v1 = core_v1_api.CoreV1Api()
    resp = createpods(core_v1, nodes,pods_details)
    return resp

