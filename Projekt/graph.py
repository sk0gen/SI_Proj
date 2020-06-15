import networkx as nx
import json
from pprint import pprint
import matplotlib.pyplot as plt
from collections import defaultdict


class graph_helper:

    def __init__(self, graph_json):
        self.graph_json = json.load(graph_json)
        self.graph_labels, self.graph_labels_len = self.get_all_labels()
        self.vertex_edges = self.vertex_and_edges()
        self.generated_csp = self.generate_csp_constraints()
        self.graph, self.edge_labels = None, None

    def get_all_labels(self):
        graph_labels = set()
        for g_node in self.graph_json:
            g_vertex = self.graph_json[g_node]
            graph_labels.add(g_node)
            for g_sub in g_vertex:
                graph_labels.add(g_sub["l"])
        return graph_labels, len(graph_labels)

    def vertex_and_edges(self):
        vertex_edges = defaultdict(list)
        for g_node in self.graph_json:
            g_vertex = self.graph_json[g_node]
            for g_sub in g_vertex:
                vertex_edges[g_node].append(g_sub["l"])
        return vertex_edges

    def generate_csp_constraints(self):

        labels_len = len(self.graph_labels)
        generated_string = ''

        # new int labels
        temp = ''
        for label in self.graph_labels:
            generated_string = generated_string + f"new_int({label},1,{labels_len})\n"
            temp = temp + f'{label},'

        generated_string = generated_string + f'int_array_allDiff([{temp[:-1]}])\n'
        # create magic label => k

        generated_string = generated_string + f'new_int(k,1,{labels_len * 10})\n'

        for key in self.vertex_edges.keys():
            temp = f'{key},'
            for edge in self.vertex_edges[key]:
                temp = temp + f'{edge},'
            temp = temp[:-1]
            generated_string = generated_string + f"int_array_plus([{temp}],k)\n"

        generated_string = generated_string + 'solve satisfy'
        return generated_string

    def generate_graph(self, json_graph):
        graph_json = json.loads(json_graph)
        graph = nx.Graph()
        edges_labels = dict()

        for g_node in graph_json:
            g_vertex = graph_json[g_node]
            for g_sub in g_vertex:
                graph.add_edge(g_node, g_sub["v"])
                g_vertex = (g_node, g_sub["v"])
                edges_labels[g_vertex] = g_sub["l"]
        self.graph = graph
        self.edge_labels = edges_labels

    def show_graph(self):
        pos = nx.spring_layout(self.graph)
        plt.figure()
        nx.draw(self.graph, pos, with_labels=True, font_weight='bold',
                labels={node: node for node in self.graph.nodes()})
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=self.edge_labels, font_color='red')
        plt.axis('off')
        plt.show()
