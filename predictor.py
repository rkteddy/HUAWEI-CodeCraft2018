from allocate import *
from parsers import *
from preprocess import *
from linear_regression import linear_regression

exponent = 0.825
addition = 0.3


def predict_vm(ecs_lines, input_lines):
    # Do your work from here#
    result = []
    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result

    sample_server, sample_machine, flavor_list, predict_span, dim_to_be_optimized = read_input(input_lines)
    history_data = read_data(ecs_lines)
    predict_cnt, predict_machine = predict(sample_machine, flavor_list, history_data, predict_span)
    server_list = assign_flavors(sample_server, predict_machine)
    # server_list = simulte_anneal_assign(sample_server, predict_machine, dim_to_be_optimized)

    result.append(str(len(predict_machine)))
    for i in range(len(flavor_list)):
        result.append("flavor" + str(flavor_list[i] + 1) + " " + str(predict_cnt[i]))
    result.append("")
    result.append(str(len(server_list)))
    for i in range(len(server_list)):
        tmp = str(i + 1) + " "
        for j in range(len(flavor_list)):
            if server_list[i].vm_cnt[flavor_list[j]] != 0:
                tmp += "flavor" + str(flavor_list[j] + 1) + " " + str(server_list[i].vm_cnt[flavor_list[j]]) + " "
        result.append(tmp)
    return result


def predict(sample_machine, flavor_list, history_data, predict_span):

    lse_model = linear_regression()
    predict_cnt = []
    predict_machine = []
    for i in flavor_list:
        predict_list = []
        # history_data[i] = avg_filter(history_data[i])
        history_data[i] = get_pow(history_data[i], exponent)
        history_data[i] = batch_add(history_data[i], addition)

        x_train, y_train, x_last = create_dataset(history_data[i], 10, 1)
        # lse_model.lse_fit(x_train, y_train)
        lse_model.ridge_fit(x_train, y_train, 0.2)

        for j in range(predict_span):
            predict_val = lse_model.predict(x_last)
            predict_list.append(predict_val)
            predict_mat = matrix(1, 1, predict_val)
            x_last.col_append(predict_mat)
            x_last.col_deque()

        predict_list = batch_add(predict_list, -addition)
        predict_list = get_pow(predict_list, 1 / exponent)

        predict_cnt.append(int(abs(sum(predict_list))))

        for k in range(predict_cnt[-1]):
            predict_machine.append([machine for machine in sample_machine if machine.num == i][0])

        print("Predict:")
        print(predict_cnt[-1])

    return predict_cnt, predict_machine
