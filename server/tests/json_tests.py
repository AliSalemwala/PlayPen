import json

def create_json(path):
    with open(path) as file:
        lines = file.read().splitlines()

    data_read = []

    for line in lines:
        data_read.append(line.split())

    append_data = []

    for index_array in data_read:
        tmp = dict()
        tmp['md5'] = index_array[0]
        tmp['timestamp'] = index_array[1]

        append_data.append(tmp)

    data_read = dict()
    data_read['files'] = append_data

    with open(path+'.json', 'a+') as file:
        json.dump(data_read, file)

    return data_read


print(json.dumps({"files":[{"md5":"14514135351","timestamp":"19:56, 01 MAR 2019"},{"md5":"98765442121","timestamp":"13:21, 25 JAN 2018"},{"md5":"65641561213","timestamp":"08:01, 30 SEP 2015"},{"md5":"74145635316","timestamp":"23:41, 15 APR 1995"},{"md5":"25665135165","timestamp":"01:01, 05 OCT 2016"}]}, sort_keys=True, indent=4))
print(json.dumps(create_json('dump')))
