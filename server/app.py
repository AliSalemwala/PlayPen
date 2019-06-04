from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
from flask_cors import CORS

from os import listdir, mkdir, system, remove
from os.path import isfile, join, isdir

import json

app = Flask(__name__)
api = Api(app)

cors = CORS(app)

PATH_NAME = "./samples/VirusSign-AllM/"

# predict
class Predict(Resource):
    def get(self, file_id):
        system("./bin/Predict.exe " + PATH_NAME + file_id)

# alert modeling
class Alert_List(Resource):
    def get(self):
        dir_list = [f for f in listdir('./logs/alerts/') if isfile(join('./logs/alerts/', f))]
        return dir_list


class Alert(Resource):
    def get(self, file_id):
        path = './logs/alerts/alerts'
        curr_logs = create_json(path)

        return curr_logs
        

class CFG(Resource):
        def get(self, dir_id, file_id):
            path = "./logs/phylogeny/cfg/" + dir_id + "/" + file_id
            #curr_logs = read_file(path)

            ret_val = create_cfg_json(path)

            if (ret_val):
                with open(path) as json_data:
                    d = json.load(json_data)

                return d
            else:
                return None


# Predict
api.add_resource(Predict, '/predict/<string:file_id>')
# alerts
api.add_resource(Alert, '/alerts/<string:file_id>/')
api.add_resource(Alert_List, '/alerts/')
# phylogeny
# cfg
api.add_resource(CFG, '/phylogeny/cfg/<string:dir_id>/<string:file_id>')

# read from file and return a list
def read_file(path):
    with open(path) as file:
        lines = file.read().replace('\n', '')

    return lines


# write to a file
def write_file(path, log):
    with open(path, 'a+') as file:
        lines = file.write(log+'\n')


def makeFileInfo(filename):
    system('./bin/readpe.sh ' + filename)
    file = open('peinfo.txt', 'r')
    html = file.read()
    file.close()
    
    system('rm peinfo.txt')
    
    return html


def create_json(path):
    check = isfile(path+'.json')

    if check:
        remove(path+'.json')

    with open(path) as file:
        lines = file.read().splitlines()

    data_read = []

    for line in lines:
        data_read.append(line.split(' ', 4))

    append_data = []

    for index_array in data_read:
        tmp = dict()
        tmp['md5'] = index_array[1]
        tmp['entropy'] = index_array[2]
        tmp['filesize'] = index_array[3]
        tmp['timestamp'] = index_array[4]
        filename = index_array[0]
        print (filename)
        html = makeFileInfo(filename)
        tmp['html'] = html

        append_data.append(tmp)

    data_read = dict()
    data_read['files'] = append_data

    with open(path+'.json', 'w') as file:
        json.dump(data_read, file)

    return data_read


def create_cfg_json(path):
    with open(path) as json_data:
        d = json.load(json_data)


    with open(path, 'w') as f:
        json.dump(d, f)
    
    return True



if __name__ == '__main__':
    app.run(debug=True)
