import json
import os


class Person:
    name = ""
    age = ""
    sex = ""
    species = ""
    occupation = ""
    descriptors = []

    def __init__(self, data):
        pass

    def gen_name(self, data):
        self.name = self.get_value(data.tables['person']['profile']['name'])

    def get_value(self, list):
        # count total weight of all items
        total_weight = 0
        for entry in list:
            # add only if this object fulfills req
            if check_req(entry['req']):
                total_weight += entry.wt

        return ""

def check_req(self, req):
    for key, vals in req:
        if getattr(self, key) not in expand(vals):
            return False

    return True

def expand(vals):
    for val in vals:


def parse_vars(str):
    pass

def parse_nums(str):
    pass

def parse_val(str):
    pass

class Data:
    tables = {}

    def __init__(self):
        self.read_data()

    def read_data(self):
        for file in os.listdir("genfiles"):
            f = open("genfiles/"+file)
            self.tables[file.replace(".json", "")] = json.load(f)


d = Data()
print(d.tables['boo'])