import collections
import json
import random
import re


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


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
        entity[key] = next(choose_options(data["resources"], options, entity, 1))

    return entity


def choose_options(res, options, entity, n):
    # keep a list of options for which the entity fulfills all requirements
    valid_options = []
    # for each option
    for opt in options:
        # check if entity fulfills all requirements
        if check_reqs(opt, entity):
            # add the option to the valid list
            valid_options.append([opt['wt'], opt['val']])

    # get a generator that returns the chosen options
    chosen = weighted_selection(valid_options, n)
    # yield each chosen option
    while n:
        # replace commands inside the value of the next chosen
        value = parse_commands(res, entity, next(chosen))

        # return the completed value
        yield value
        n -= 1


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
def parse_commands(res, entity, string):
    string = parse_selection(res, entity, string)
    string = parse_numeric(string)

    return string


# selection command: $...$
# returns a string with instances of a selection command replaced by a value selected by the command
# res is the list of resources that the selection command will pull from
# entity is the entity being generated as it currently exists, used for checking against requirements
def parse_selection(res, entity, string):
    # get list of all matches
    matches = re.findall("\$(.*?)\$", string)
    # unique list
    match_set = set(matches)
    # for each unique match
    for match in match_set:
        # get number of occurrences in original string
        occurences = matches.count(match)
        # get replacement values
        replacements = choose_options(res, res[match], entity, occurences)
        # for each occurence
        for i in range(occurences):
            # replace command with a unique replacement value
            string = string.replace('$'+match+'$', next(replacements), 1)

    return string


# numeric generation command: [...]
# returns a string with instances of a numeric generation command replaces with a number generated from the command
# string is the string that will be parsed
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


# checks an entity to ensure that it follows all requirements in options
# options is the option that entity is being checked against to see if it meets the requirements
# entity is the entity that is being checked against the requirements of option
def check_reqs(option, entity):

    # for each key in requirements
    for key, values in option["req"].items():
        if not check_attr(values, entity, key):
            # return that one or more requirements were not met
            return False

    # if no attribute requirements went unfulfilled, return that all requirements were met
    return True


# checks whether an attribute on entity matches any one of the possible values for the requirement
# vals is the list of possible values that entity[attr] can have
# entity is the entity being checked
# attr is the particular attribute being checked on the entity
def check_attr(vals, entity, attr):
    # if it meets one of the requirements, return True
    for value in vals:
        if check_req(value, entity, attr):
            return True

    # if it met none of the requirements, return False
    return False


# checks whether exactly one possible value of a requirement matches the corresponding attribute attr on entity
# req is the value that is being compared to entity[attr]
# entity is the entity that is attempting to fulfill the requirement
# attr is the attribute of entity that must match the value of req
def check_req(req, entity, attr):

    compare_nums = re.match("\[(<|>|<=|>=|=)([0-9]+)\]", req)
    # if the value is a numeric comparison
    if not compare_nums is None:
        try:
            num(entity[attr])
        except ValueError:
            print("Attempted to do a numeric comparison on a non-numeric entity attribute: "+entity.type+"["+attr+"]")

        return compare(compare_nums.group(1), entity[attr], compare_nums.group(2))
    # if the requirement is a straight text comparison
    else:
        if entity[attr] == req:
            return True
        else:
            return False


# takes 3 strings
# operator is a string containing the operator to use for comparison (one of =, <, <=, >, >=)
# a and b are the values that will be compared
# both a and b must be numeric
def compare(operator, a, b):
    if operator == "=":
        return num(a) == num(b)
    elif operator == "<":
        return num(a) < num(b)
    elif operator == "<=":
        return num(a) <= num(b)
    elif operator == ">":
        return num(a) > num(b)
    elif operator == ">=":
        return num(a) >= num(b)