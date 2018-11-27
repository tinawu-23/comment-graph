import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab

G = nx.DiGraph()

with open('.\\redditJson\\bunny.json') as f:
    data = json.load(f)

for index, reply in enumerate(data):
    curnode = reply['body']
    G.add_node(curnode)
    if reply['parent']:
        for i in range(index+1):
            if reply['parent'] == data[index-i]['author_name']:
                G.add_edges_from([(data[index-i]['body'],reply['body'])])

edge_labels = dict([((u, v,)) for u, v, d in G.edges(data=True)])

pos = nx.spring_layout(G)
node_labels = {node: node for node in G.nodes()}
nx.draw(G, pos, node_color='red', node_size=1500,
        edge_color='black', edge_cmap=plt.cm.Reds)
nx.draw_networkx_labels(G, pos, labels=node_labels)
pylab.show()
