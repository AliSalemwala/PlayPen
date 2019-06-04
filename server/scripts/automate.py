import random
import sys
import os

INTERVAL = 15

def run(iters, port):
    malware_file = open('../malware_list', 'r')
    malware_ls = malware_file.read().split('\n')
    malware_file.close()

    url = "localhost:" + port +"/predict/"

    size = len(malware_ls)

    index = 0
    for i in range (0, iters):
        index += INTERVAL
        fullpath = url + (malware_ls[index].split('/')[-1])
        print(str (index) + ") Querying: " + fullpath)
        os.system("curl " + fullpath + " -X GET")

if __name__ == '__main__':
        port = sys.argv[1]
        iterations = int(sys.argv[2])

        run(iterations, port)

