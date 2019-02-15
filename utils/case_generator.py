import json
import random


class CaseGenerator(object):
    def __init__(self,header, number=100, params_size=None,params_type='int', max_params_size=10000, ordered=False):
        self.number = number
        self.params_type = params_type
        self.params_size = params_size
        self.header = header

    def generator(self):
        self.data = []
        if not self.params_size:
            for i in range(self.number):
                size = random.randint(0,20001)

                row = random.sample([i for i in range(size)],size//2)
                self.data.append(row)
        else:
            for i in range(self.number):
                size = 2 * self.params_size
                row = random.sample([i for i in range(size)],size//2)
                self.data.append(row)

    def write(self):
        with open(self.header + '.json', 'wt') as f:
            jsons = json.dumps(self.data)
            f.write(jsons)


c = CaseGenerator(header='A+B Problem', params_size=2)
c.generator()
c.write()