import collections
import json
import random
import re


# load a json file into a dictionary
def load_json(filename):
    f = json.load(open(filename), object_pairs_hook=collections.OrderedDict)
    return f


# generate an entity from a json profile
def generate_entity(data):
    # generate a blank entity
    entity = {}
    # for each key in the data profile
    for key, options in data["profile"].items():
        # generate a value for the entity according to the list of options
        entity[key] = choose_option(data, options, entity)

    return entity


def choose_option(data, options, entity):
    # keep a list of options for which the entity fulfills all requirements
    valid_options = []
    # for each option
    for opt in options:
        # check if entity fulfills all requirements
        if check_req(opt, entity):
            # add the option to the valid list
            valid_options.append([opt['wt'], opt['val']])

    # select one of the valid options and store its value
    chosen = next(weighted_selection(valid_options, 1))

    # replace commands inside the value of chosen
    chosen = parse_commands(data, entity, chosen)

    # return the completed value
    return chosen


def weighted_selection(items, n):
    total = float(sum(w for w, v in items))
    i = 0
    w, v = items[0]
    while n:
        x = total * (1 - random.random() ** (1.0 / n))
        total -= x
        while x > w:
            x -= w
            i += 1
            w, v = items[i]
        w -= x
        yield v
        n -= 1

"""
def weighted_selection(options):
    # keep track of total weight of all options
    total_weight = 0
    # for each option
    for opt in options:
        # update the total_weight
        total_weight += opt["wt"]

    # generate a random integer between 0 and total_weight
    number = random.randint(0, total_weight)

    # select the option that corresponds to the generated number
    current_weight = 0
    index = 0
    while number > current_weight:
        current_weight += options[index]['wt']
        index += 1
    # return the selected option
    return options[index]
"""


# removes all command syntax from a string, replacing it with a valid value for that command
def parse_commands(data, entity, string):
    string = parse_selection(data, entity, string)
    string = parse_numerical(string)

    return string


# selection command: $...$
def parse_selection(data, entity, string):
    while True:
        # break when no more replacements are needed
        matches = re.search("\$(.*?)\$", string)
        if matches is None:
            break
        # get replacement value
        replacement = choose_option(data, data["resources"][matches.group(1)], entity)
        # replace command with its replacement value
        string = string.replace(matches.group(0), replacement)

    return string


# numerical generation command: [...]
def parse_numerical(string):
    while True:
        # break when no more replacements are needed
        matches = re.search("\[([0-9]*)\-([0-9]*)\]", string)
        if matches is None:
            break
        # generate replacement value
        replacement = str(random.randint(int(matches.group(1)), int(matches.group(2))))
        # replace command with its replacement value
        string = string.replace(matches.group(0), replacement)

    return string


def check_req(option, entity):
    # for each key in requirements
    for key, values in option["req"].items():
        # check the entity's key of the same name
        # if the value stored in entity[key] is not in the list of valid
        # options in option["req"][key]
        if entity[key] not in values:
            # return that one or more requirements were not met
            return False

    # if no requirements went unfulfilled, return that all requirements were met
    return True