#!/bin/bash
#
# Monitor overall Kubernetes cluster utilization and capacity.
#
# Original source:
# https://github.com/kubernetes/kubernetes/issues/17512#issuecomment-367212930
#
# Tested with:
#   - AWS EKS v1.11.5
#
# Does not require any other dependencies to be installed in the cluster.

set -e

REQ_CPU=8
REQ_REM=20
REQ_GPU=0
KUBECTL="kubectl"
NODES=$($KUBECTL get nodes --no-headers -o custom-columns=NAME:.metadata.name)
function usage() {
  local node_count=0
  local total_available_gpu=0
  local readonly nodes=$@

  for n in $nodes; do
    local num=1000
    local checks=$($KUBECTL get nodes $n --no-headers -o custom-columns=LABELS:.metadata.labels.hardware-type)
    local check_zone=$($KUBECTL get nodes $n --no-headers -o custom-columns=LABELS:.metadata.labels.zone)

    if [[ "$check_zone" != "master" ]]
    then
      local capacity_cpus=$($KUBECTL describe node $n | grep -A1 "Capacity" | tail -n1)    
      local total_cpus=$(echo $capacity_cpus | awk '{print $2}') 

      local capacity_mem=$($KUBECTL describe node $n | grep -A5 "Capacity" | tail -n1)
      local get_mem=$(echo $capacity_mem | awk '{print $2}')
      local total_mem=$(echo $(echo $get_mem | awk '{t=length($0)}END{print substr($0,0,t-2)}')/$num | bc)

      local requests_cpu_mem=$($KUBECTL describe node $n | grep -A3 -E "\\s\sRequests" | tail -n2)
      local reserved_cpu=$(echo $requests_cpu_mem | awk -F "[(m)]" '{print $4}')
      local total_available_mem=0
      local get_reserved_mem=$(echo $requests_cpu_mem | awk '{print $9}')
      local reserved_mem=$(echo $get_reserved_mem | awk '{t=length($0)}END{print substr($0,0,t-2)}' | bc)
    
      if [[ -n "$reserved_mem" ]]
      then
        total_available_mem=$(echo $total_mem - $reserved_mem | bc)
      else
        total_available_mem=$total_mem
      fi
   
      local total_cpus_m=`expr $total_cpus \* $num`
      local total_available_cpus=`expr $total_cpus_m \- $reserved_cpu`
    

      if [[ ${checks} = NVIDIAGPU ]]
      then
        local capacity=$($KUBECTL describe node $n | grep -A6 "Capacity" | tail -n1)
        local requests=$($KUBECTL describe node $n | grep -A7 -E "\\s\sRequests" | tail -n1)
        local capacity_gpu=$(echo $capacity | awk '{print $2}')
        local requested_gpu=$(echo $requests | awk '{print $2}')
      else
        local capacity_gpu=0
        local requested_gpu=0
      fi
 
      total_available_gpu=$((capacity_gpu - requested_gpu))

      if [[ $(echo $total_available_cpus/$num | bc) -ge $REQ_CPU ]] && [[ $(echo $total_available_mem/$num | bc) -ge $REQ_REM ]] && [[ $total_available_gpu -ge $REQ_GPU ]]
      then
        echo "================================================"
        echo "Node: $n"
        echo "================================================"
        echo "Total Available CPUs = $(echo $total_available_cpus/$num | bc)"
        echo "Total Available Memory(GB) = $(echo $total_available_mem/$num | bc)"
        echo "Total Available GPUs = ${total_available_gpu}"
        echo "Node's Zone = ${check_zone}"
      fi
    fi
  done
  echo "================================================"

}

usage $NODES
