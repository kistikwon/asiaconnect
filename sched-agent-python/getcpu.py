from subprocess import call,check_output
import math

def cpu_capacity(args):
    get_cpu_capacity='kubectl describe node '+args+' | grep -A1 "Capacity" | tail -n1'+' | awk \'{print $2}\''
    check_cpu=check_output([get_cpu_capacity], shell=True)
    capacity_cpu=(int(check_cpu.decode("utf-8"))*1000)
    return(capacity_cpu)

def cpu_used(args):
    get_cpu_used='kubectl describe node '+args+' | grep -A2 -E "\\s\sRequests" | tail -n1 | awk  \'{print $2}\''
    check_used_cpu=check_output([get_cpu_used], shell=True)
    check_used_cpu=(check_used_cpu.decode("utf-8")).strip()
    if(check_used_cpu != '0'):
      used_cpu=int(check_used_cpu[:-1])
    else:
      used_cpu=int(check_used_cpu)
    return(used_cpu)

