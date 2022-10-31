from subprocess import call,check_output
import math

def memory_capacity(args):
    get_mem_capacity='kubectl describe node '+args+' | grep -A5 "Capacity" | tail -n1'+' | awk \'{print $2}\''
    check_mem=check_output([get_mem_capacity], shell=True)
    capacity_mem=(int((check_mem.decode("utf-8"))[:-3])/1000)
    return(capacity_mem)

def memory_used(args):
    get_mem_used='kubectl describe node '+args+' | grep -A3 -E "\\s\sRequests" | tail -n1 | awk  \'{print $2}\''
    check_used_mem=check_output([get_mem_used], shell=True)
    check_used_mem=(check_used_mem.decode("utf-8")).strip()
    if(check_used_mem != '0'):
      used_mem=int(check_used_mem[:-2])
    else:
      used_mem=int(check_used_mem)
    return(used_mem)

