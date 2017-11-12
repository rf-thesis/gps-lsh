import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

G = nx.read_edgelist("gephi/edge-list.csv", delimiter=",", data=[("weight", float)])
edge_labels = dict( ((u, v), d["weight"]) for u, v, d in G.edges(data=True) )
pos = nx.random_layout(G)
nx.draw(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
# plt.show()

positions = pd.DataFrame(pos).transpose()

positions.columns = ['X','Y']
positions.to_csv('nodepositions.csv', encoding='utf-16', index_label='ID')

# inputedges = pd.read_csv('gephi/edge-list.csv')
# inputnodes = pd.read_csv('gephi/node-list.csv')

# for i,r in inputnodes.iterrows():
#     G.add_node(r['id'])
    
# for i,r in inputedges.iterrows():
#     G.add_edge(r['source'],r['target'], weight=r['weight'])

# pos=nx.spring_layout(G, k=0.04, iterations=10, scale=100)

# nx.set_node_attributes(G,'pos',pos)

# pos[-2] = [100.0, 0.0]
# pos[-1] = [0.0, 100.0]


# nx.draw(G, pos=pos)
plt.savefig("network_graph.png")
plt.show()
