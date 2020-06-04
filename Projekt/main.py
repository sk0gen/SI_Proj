import networkx as nx
import json
from pprint import pprint
import matplotlib.pyplot as plt
from collections import defaultdict
import os
from graph import graph_helper
import consts

constraints_filename = "Data/constraints.txt"
result_filename = "Data/result.txt"
graph_json_filename = "Data/graph2.json"


def get_result_string():
    to_return = None
    with open(result_filename, 'r') as result_file:
        to_return = result_file.read()
    to_return = to_return.replace(consts.to_delete, "")
    to_return = to_return.replace(consts.to_delete2, "")
    return to_return


def result_string_to_dict(result_string):
    temp = result_string.split('\n')
    temp = temp[:-1]
    dictionary = dict()
    for x in temp:
        key_value = x.split(' = ')
        dictionary[key_value[0]] = key_value[1]
    return dictionary


if __name__ == '__main__':
    graph_help = None
    with open(graph_json_filename) as graph:
        graph_help = graph_helper(graph)

    with open(constraints_filename, 'w') as result_file:
        result_file.write(graph_help.generated_csp)
    os.system(f'./BumbleBEE {constraints_filename} > {result_filename} ')
    os.system(f'./BumbleBEE {constraints_filename} -dimacs dimacs.cnf dimacs.map')

    result = get_result_string()
    result_dictionary = result_string_to_dict(result)

    result_json = None
    with open(graph_json_filename) as graph:
        result_json = graph.read()
        for x in result_dictionary:
            result_json = result_json.replace(x, result_dictionary[x])

    graph_help.generate_graph(result_json)
    graph_help.show_graph()
