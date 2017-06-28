'''
Given input of a fixed k, checks whether the cop number of a graph,
G, is less than or equal to k.
'''
import networkx as nx

k = input('Enter a k to check: ')

#Test code for the 5 cycle graph
#TODO: Implement user input graphs
G = nx.cycle_graph(5)

#Add self loops at each vertex
for node in G.nodes():
    G.add_edge(node, node)

def kproduct(graph):
    '''
    Applies the tensor product to graph k-1 times.

    INPUT:
    graph: A networkx graph

    OUTPUT
    tens: The graph on which the tensor product has been applied k-1 times.
    '''

    tensor = graph.copy()

    for i in range(0, k-1):
        tensor = nx.tensor_product(tensor, graph)
        
    return tensor

#Get the k-1th tensor product and then create the set on which we make our elimination 

P = kproduct(G)
print P.nodes()
elim = nx.tensor_product(P, G)

