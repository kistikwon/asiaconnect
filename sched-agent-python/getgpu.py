from subprocess import call,check_output
import math

def gpu_capacity(args):
    get_gpu_capacity='kubectl describe node '+args+' | grep -A6 "Capacity" | tail -n1'+' | awk \'{print $2}\''
    check_gpu=check_output([get_gpu_capacity], shell=True)
    capacity_gpu=int(check_gpu.decode("utf-8"))
    return(capacity_gpu)

def gpu_used(args, position):
    get_gpu_used='kubectl describe node '+args+' | grep -A'+position+' -E "\\s\sRequests" | tail -n1 | awk  \'{print $2}\''
    check_used_gpu=check_output([get_gpu_used], shell=True)
    check_used_gpu=(check_used_gpu.decode("utf-8")).strip()
    used_gpu=int(check_used_gpu)
    return(used_gpu)

