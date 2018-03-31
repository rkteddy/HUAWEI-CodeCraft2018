import copy
import random
import math

# physical server class definition
class physical_server:

    def __init__(self, cpu, mem):
        self.cpu = cpu
        self.rest_cpu = cpu
        self.mem = mem
        self.rest_mem = mem
        self.vm_cnt = [0 for i in range(15)]
        self.cpu_usage_rate = 1 - float(self.rest_cpu) / float(self.cpu)
        self.mem_usage_rate = 1 - float(self.rest_mem) / float( self.mem)

    def add_vm(self, vm):
        self.vm_cnt[vm.num] += 1
        self.rest_cpu -= vm.cpu
        self.rest_mem -= vm.mem
        self.cpu_usage_rate = 1 - float(self.rest_cpu) / float(self.cpu)
        self.mem_usage_rate = 1 - float(self.rest_mem) / float( self.mem)


# virtual machine class definition
class virtual_machine:

    def __init__(self, num, cpu, mem):
        self.num = num
        self.cpu = cpu
        self.mem = mem
        self.cnt = 0


def isable_locate(server, machine):
    if machine.cpu > server.rest_cpu or machine.mem > server.rest_mem:
        return False
    else:
        return True


def assign_flavors(sample_server, machine_list):
    server_list = [copy.deepcopy(sample_server)]
    for i in range(len(machine_list)):
        j = 0
        while j < len(server_list) and not isable_locate(server_list[j], machine_list[i]):
            j += 1
        if j < len(server_list) and isable_locate(server_list[j], machine_list[i]):
            server_list[j].add_vm(machine_list[i])
        else:
            server_list.append(copy.deepcopy(sample_server))
            server_list[-1].add_vm(machine_list[i])

    # for i in range(len(server_list)):
    #     print("Server " + str(i+1) + ": ")
    #     for j in range(len(server_list[i].vm_cnt)):
    #         print(server_list[i].vm_cnt[j])

    return server_list


