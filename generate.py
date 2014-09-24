import json
import random
import re


# load a json file into a dictionary
def load_json(filename):
    f = json.load(open(filename))
    return f


# generate an entity from a json profile
def generate(data):
    # generate a blank entity
    entity = {}
    # for each key in the data profile
    for key, value in data["profile"]:
        # generate a value for the entity according to the list of options
        entity[key] = ""


def extract(data, options, entity):
    # keep track of total weight of all options
    total_weight = 0
    # keep a list of options for which the entity fulfills all requirements
    valid_options = []
    # for each option
    for opt in options:
        # check if entity fulfills all requirements
        if check_req(opt, entity):
            # add the option to the valid list
            valid_options.append(opt)
            # update the total_weight
            total_weight += opt["wt"]

    # generate a random integer between 0 and total_weight
    number = random.randint(0, total_weight)
    # select the option that corresponds to the generated number
    current_weight = 0
    index = 0
    while number < current_weight:
        current_weight += valid_options[index]['wt']
        index += 1
    # store the selected option
    chosen = valid_options[index]['val']

    # now replace commands inside the value of chosen
    # selection command: $...$
    while True:
        # break when no more replacements are needed
        matches = re.search("$(.*?)$")
        if matches is None:
            break
        # get replacement value
        replacement = extract(data, data["resources"][matches.group(1)], entity)
        # replace command with its replacement value
        re.sub(matches.group(0), replacement)

    # numerical generation command: [...]
    # TODO

    # return the completed value
    return chosen


def check_req(option, entity):
    # for each key in requirements
    for key, values in option["req"]:
        # check the entity's key of the same name
        # if the value stored in entity[key] is not in the list of valid
        # options in option["req"][key]
        if entity[key] not in values:
            # return that one or more requirements were not met
            return False

    # if no requirements went unfulfilled, return that all requirements were met
    return True