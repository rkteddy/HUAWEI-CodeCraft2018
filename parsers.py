from allocate import physical_server
from allocate import virtual_machine

days_of_month = [31, 30, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

global predict_begin
global predict_end
global flavor_list


def read_input(input_lines):
    global history_begin
    global predict_begin
    global predict_end
    global flavor_list
    sample_server = []
    sample_machine = []
    flavor_list = []
    flavor_cnt = 0
    now_block = 0
    CPU = 0
    MEM = 0
    for index in range(len(input_lines)):
        if index == 0:
            items = input_lines[index].split(" ")
            CPU = int(items[0])
            MEM = int(items[1]) * 1024
            sample_server = physical_server(CPU, MEM)
        elif index == 1:
            flavor_cnt = int(input_lines[index])
        elif 1 < index <= 1 + flavor_cnt:
            items = input_lines[index].split(" ")
            NUM = int(items[0][6:]) - 1
            CPU = int(items[1])
            MEM = int(items[2])
            tempVM = virtual_machine(NUM, CPU, MEM)
            sample_machine.append(tempVM)
            flavor_list.append(NUM)
        elif index == 2 + flavor_cnt:
            dim_to_be_optimized = input_lines[index].split("\n")[0]
        elif index == 3 + flavor_cnt:
            predict_begin = input_lines[index].split(" ")[0]
        elif index == 4 + flavor_cnt:
            predict_end = input_lines[index].split(" ")[0]

    return sample_server, sample_machine, flavor_list, time2val(predict_end)-time2val(predict_begin), dim_to_be_optimized


def read_data(ecs_lines):
    first_line = ecs_lines[0].split("\t")
    history_begin = first_line[2]
    last_line = ecs_lines[-1].split("\t")
    history_end = last_line[2]

    history_data = [[.0] for i in range(22)]
    for i in flavor_list:
        for j in range(time2val(history_begin), time2val(history_end)):
            history_data[i].append(0)

    # Read history data
    for line in ecs_lines:
        if len(line.strip()):
            items = line.split("\t")
            temp_flavor = int(items[1][6:]) - 1
            temp_time = items[2]
            if temp_time is not None:
                value = time2val(temp_time) - time2val(history_begin)
                if temp_flavor in flavor_list:
                    history_data[temp_flavor][value] += 1
                else:
                    pass
            else:
                print('Time data error.\n')

    # Print history data
    print('History data: ')
    print('Total diffs: ' + str(len(history_data[0])))
    for i in flavor_list:
        print('Flavor' + str(i + 1) + ': (Total: ' + str(sum(history_data[i])) + ')\n' + str(history_data[i]) + '\n')

    return history_data


def time2val(time):
    year = time[0:4]
    month = time[5:7]
    day = time[8:10]

    # Convertion
    year = 365 * (int(year) - 2000)
    month = int(month)
    day = int(day)

    # To value
    value = 0
    month -= 1
    for i in range(0, month):
        value += days_of_month[i + 1]
    value += (day - 1) + year

    return value