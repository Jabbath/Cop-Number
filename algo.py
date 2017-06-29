'''
Given input of a fixed k, checks whether the cop number of a graph,
G, is less than or equal to k.
'''
import networkx as nx
from copy import deepcopy

k = input('Enter a k to check: ')

#Test code for the 5 cycle graph
#TODO: Implement user input graphs
G = nx.petersen_graph()
Gnodes = set(G.nodes())

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

def extractVertices(vertex):
    '''
    Given a vertex resulting from a tensor product,
    extracts each component of the vertex.

    INPUT
    vertex: A nest of 2-tuples

    OUTPUT
    components: A list of of the vertices nested in vertex
    '''
    
    #There are k - 1 nests because the tensor product is applied k-1 times
    levels = k - 1
    
    #In this case the tensor product was not applied and vertex is not a tuple
    if levels == 0:
        return [vertex]

    components = [vertex[1]]
    curNest = vertex[0]

    #Go through each nest and take the vertices
    for i in range(0, levels):
        
        #If the current nest is not a tuple we have hit the last layer
        if not isinstance(curNest, tuple):
            components.append(curNest)
            break

        components.append(curNest[1])
        curNest = curNest[0]

    return components 
        
def Gneighborhood(vertex):
    '''
    Given a vertex from a tensor product,
    returns the neighborhood of each component
    vertex in G.

    INPUT
    vertex: A vertex from a tensor product

    OUTPUT
    neighborhood: A set of all vertices in the G neighborhood
    of the components of vertex
    '''
    neighborhood = set()

    #We want to get every component of vertex. It is a nest of two tuples
    subvertices = extractVertices(vertex)
    
    #Go through each vertex and get it's neighbors
    for vertex in subvertices:

        #The ego graph returns the neighbors of vertex in G
        neighbors =  nx.ego_graph(G, vertex).nodes()
        neighborhood.update(neighbors)
    
    return neighborhood


#Get the kth tensor product
P = kproduct(G)
Pnodes = set(P.nodes())

#Make a dict where the keys are vertices of P and entries are their G neighbors
NG = {}

for node in Pnodes:
    NG[str(node)] = Gneighborhood(node)

def NGSet(vertexSet):
    '''
    Given a set of vertices in P, returns the union of 
    their G neighborhoods.

    INPUT
    vertexSet: A set of vertices in P

    OUTPUT
    setNeighborhood: The G neighborhood of vertexSet
    '''
    setNeighborhood = set()

    #Add on each vertex's neighborhood
    for vertex in vertexSet:
        setNeighborhood.update(set(nx.ego_graph(G, vertex).nodes()))

    return setNeighborhood


def checkChange(fOld, fNew):
    '''
    Given an old set for f, and a new one,
    checks whether they have any values that are different.

    INPUT
    fOld: f before modification
    fNew: f after modification

    OUTPUT
    dif: Boolean value whether fOld = fNew
    '''
    dif = False
    
    #Go through each vertex and compare the sets
    for vertex in fOld:
        
        #A^B = {} iff A = B
        if len(fOld[vertex] ^ fNew[vertex]) != 0:
            dif = True
            break

    return dif
#Create f given on page 120 of The Game of Cops and Robbers on Graphs
f = {}

for node in Pnodes:
    f[str(node)] = Gnodes - NG[str(node)]

#Now we want to check update f according to property 2 on page 120
#We want to keep updating until f stops changing or f(u) = {}
changing = True
empty = False
fOld = deepcopy(f)

while changing:

    #Check if f has any extra values that don't fit prop 2
    for edge in P.edges():
        source = str(edge[0])
        target = str(edge[1])

        #Update f
        f[source] = f[source] & NGSet(f[target])
        f[target] = f[target] & NGSet(f[source])
        
        #Stop if we have made an empty set
        if len(f[source]) == 0 or len(f[target]) == 0:
            changing = False
            empty = True
            break
    
    #If we haven't already found an empty f(u) check if f has changed
    if not empty:
        
        #Stop if f hasn't changed
        if not checkChange(fOld, f):
            changing = False
        else:
            fOld = deepcopy(f)

#Now check if there are any empty values for f
if not empty:
    for vertex in f:
        if len(f[vertex]) == 0:
            empty = True

if empty:
    print 'The cop number is <=', k
else:
    print 'The cop number is >', k
