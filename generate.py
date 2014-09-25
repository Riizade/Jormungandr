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
        entity[key] = next(choose_options(data, options, entity, 1))

    return entity


def choose_options(data, options, entity, n):
    # keep a list of options for which the entity fulfills all requirements
    valid_options = []
    # for each option
    for opt in options:
        # check if entity fulfills all requirements
        if check_req(opt, entity):
            # add the option to the valid list
            valid_options.append([parse_weight({}, opt['wt']), opt['val']])

    # get a generator that returns the chosen options
    chosen = weighted_selection(valid_options, n)
    # yield each chosen option
    while n:
        # replace commands inside the value of the next chosen
        value = parse_commands(data, entity, next(chosen))

        # return the completed value
        yield value
        n -= 1


# parses the expression that represents the weight of an object, and evaluates the expression to return an integer
# returns: integer
def parse_weight(context, weight):
    # replace selection commands in the expression
    # get list of all matches
    matches = re.findall("\$(.*?)\$", weight)
    # unique list
    match_set = set(matches)
    # for each unique match
    for match in match_set:
        # replace command with its replacement value
        try:
            weight = weight.replace('$'+match+'$', context[match])
        except KeyError:
            weight = weight.replace('$'+match+'$', "1")

    # evaluate the expression with constants
    # THIS IS SUPER UNSAFE, WILL EXECUTE ARBITRARY CODE
    return eval(weight)


# weighted selection without replacement
def weighted_selection(items, n):
    total_weight = float(sum(wt for wt, val in items))
    while n:
        index = 0
        running_weight = items[0][0]
        rand_num = random.random() * total_weight
        while rand_num > running_weight:
            index += 1
            running_weight += items[index][0]
        wt, val = items.pop(index)
        total_weight -= wt
        yield val


# removes all command syntax from a string, replacing it with a valid value for that command
def parse_commands(data, entity, string):
    string = parse_selection(data, entity, string)
    string = parse_numeric(string)

    return string


# selection command: $...$
def parse_selection(data, entity, string):
    # get list of all matches
    matches = re.findall("\$(.*?)\$", string)
    # unique list
    match_set = set(matches)
    # for each unique match
    for match in match_set:
        # get number of occurrences in original string
        occurences = matches.count(match)
        # get replacement values
        replacements = choose_options(data, data["resources"][match], entity, occurences)
        # for each occurence
        for i in range(occurences):
            # replace command with a unique replacement value
            string = string.replace('$'+match+'$', next(replacements), 1)

    return string


# numerical generation command: [...]
def parse_numeric(string):
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