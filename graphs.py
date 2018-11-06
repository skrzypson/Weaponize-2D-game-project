import numpy as np
import networkx as nx
import community
import matplotlib.pyplot as plt

g = nx.Graph()

node_list = [node_no for node_no in range(1,10)]

g.add_nodes_from(node_list, int(x_coord=np.random.ranf()*1000), int(y_coord=np.random.ranf()*500), fraction=None, color=None)

g.add_edges_from([(1,2,{'weight': 1}),
                  (1,3,{'weight': 1}),
                  (4,5,{'weight': 1}),
                  (6,3,{'weight': 1}),
                  (2,5,{'weight': 1}),
                  (1,8,{'weight': 1})
                  ])

part = community.best_partition(g)

def return_fraction_color(fraction):
    if fraction <= 6:
        return {
            0: 'skyblue',
            1: 'blue',
            2: 'red',
            3: 'green',
            4: 'yellow',
            5: 'orange',
            6: 'black',
        }[fraction]
    else:
        return 'white'

for key in part:
    g.nodes[key]['fraction'] = part[key]
    g.nodes[key]['color'] = return_fraction_color(part[key])

print(part)
print("g: " + str(g.nodes))
print(list(g.nodes.values()))
x = g.nodes.values()
y = [node['color'] for node in x]
print("y: "+ str(y))

nx.draw(g, node_color=y, with_labels=True, font_weight='bold')

plt.show()

g.add_edges_from([(2,8,{'weight': 1})
                     , (3,4,{'weight': 1})
                     , (4,6,{'weight': 1})
                     , (5,8,{'weight': 1})
                     , (7,8,{'weight': 1})
                     , (6,8,{'weight': 1})
                  ])

nx.draw(g, with_labels=True, font_weight='bold')
plt.show()

part = community.best_partition(g)
print(part)