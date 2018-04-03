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


def get_two_different_randint(min, max):
    i = random.randint(min, max)
    j = random.randint(min, max)
    while j == i:
        j = random.randint(min, max)
    return i, j


def simulte_anneal_assign(sample_server, machine_list, dim_to_be_optimized):
    min_score = len(machine_list) + 1
    server_list = []
    T = 100
    Tmin = 1
    r = 0.9
    min_score_list = []
    server_list_list = []

    while T > Tmin:
        i, j = get_two_different_randint(0, len(machine_list) - 1)
        new_machine_list = copy.deepcopy(machine_list)
        new_machine_list[i], new_machine_list[j] = new_machine_list[j], new_machine_list[i]
        new_server_list = assign_flavors(sample_server, new_machine_list)

        if "CPU" in dim_to_be_optimized:
            machine_cpu = 0
            for i in range(len(machine_list)):
                machine_cpu += machine_list[i].cpu
            server_cpu = len(new_server_list) * sample_server.cpu
            score = len(new_server_list) - 1 + new_server_list[-1].cpu_usage_rate
        elif "MEM" in dim_to_be_optimized:
            score = len(new_server_list) - 1 + new_server_list[-1].mem_usage_rate
        else:
            print("Wrong dimension")

        if score < min_score:
            min_score = score
            machine_list = new_machine_list
            server_list = new_server_list
        else:
            if (math.exp(min_score - score) / T) > (random.randint(0, 10000) / 10000):
                min_score_list.append(min_score)
                server_list_list.append(server_list)
                min_score = score
                machine_list = new_machine_list
                server_list = new_server_list

        T = r * T

    min_index = min_score_list.index(min(min_score_list))
    server_list = server_list_list[min_index]
    print(min(min_score_list))

    return server_list
