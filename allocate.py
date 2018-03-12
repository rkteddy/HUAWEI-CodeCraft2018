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
