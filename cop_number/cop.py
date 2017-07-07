'''
Given input of a fixed k, checks whether the cop number of a graph,
G, is less than or equal to k.
'''
import networkx as nx
from copy import deepcopy

def kproduct(graph):
    '''
    Applies the tensor product to graph k-1 times.

    INPUT:
    graph: A networkx graph

    OUTPUT
    tensor: The graph on which the tensor product has been applied k-1 times.
    '''
    tensor = graph.copy()

    for i in range(0, k-1):
        tensor = nx.tensor_product(tensor, graph)
       
    return tensor

def isOriginal(vertex):
    '''
    Goes through all the vertices of the original graph G,
    and checks if vertex is one of them.

    INPUT
    vertex: A hashable object representing a vertex
    
    OUTPUT
    original: A boolean value on whether vertex is one of the originals
    '''
    original = False
    
    #Go through all of G's nodes and check if they are equal to vertex
    for node in G.nodes():
        if node == vertex:
            original = True
            break

    return original

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
        if isOriginal(curNest):
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
    
    #Check if we are dealing with just one vertex
    if isOriginal(vertex):
        subvertices = [vertex]
    else:
        #We want to get every component of vertex. It is a nest of two tuples
        subvertices = extractVertices(vertex)
    
    #Go through each vertex and get it's neighbors
    for vertex in subvertices:

        #The ego graph returns the neighbors of vertex in G
        neighbors =  nx.ego_graph(G, vertex).nodes()
        neighborhood.update(neighbors)
    
    return neighborhood

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
        setNeighborhood.update(NG[str(vertex)])
    
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

def getCopNumber():
    '''
    Finds the cop number of G by the algorithm on pg. 122
    of The Game of Cops and Robbers on Graphs.

    OUTPUT
    greater: True is the cop number is greater than k and false otherwise
    '''
    #Now we want to check update f according to property 2 on page 120
    #We want to keep updating until f stops changing or f(u) = {}
    changing = True
    empty = False
    fOld = deepcopy(f)

    while changing:
    
        print 'Starting new f update'
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
    
    #The existence of empty values for f means the cop number <= k
    if empty:
        return False
    else:
        return True

Gnodes = set()

P = nx.Graph()
Pnodes = set()

NGP = {}
NG = {}
f = {}

def initGraph():
    '''
    Makes sure the initial graph is reflexive and creates the tensor
    products, neighborhoods, and initializes f.
    '''
    #Let us use the globals for Gnodes, P, and Pnodes
    global Gnodes
    global P
    global Pnodes

    Gnodes = set(G.nodes())

    #Add self loops at each vertex
    for node in G.nodes():
        G.add_edge(node, node)
    
    #Get the kth tensor product
    P = kproduct(G)
    Pnodes = set(P.nodes())

    #Make a dict where the keys are vertices of P and entries are their G neighbors
    for node in Pnodes:
        NGP[str(node)] = Gneighborhood(node)

    #Now make a dict for the neighborhood of all the vertices of G
    for node in Gnodes:
        NG[str(node)] = Gneighborhood(node)

    #Create f given on page 120 of The Game of Cops and Robbers on Graphs
    for node in Pnodes:
        f[str(node)] = Gnodes - NGP[str(node)]


#If we are running from the cmd line use arguments
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 3:
        print 'The format for the arguments is: graphFileLocation k'
        exit()
    k = int(sys.argv[2])

    G = nx.read_multiline_adjlist(sys.argv[1])
    initGraph()
    numK = getCopNumber()

    if numK:
        print 'The cop number is >', k
    else:
        print 'The cop number is <=', k

G = 0
k = 0
#Otherwise we are using a module
def copk(graph, kVal):
    global G, k
    
    #Set globals for the module
    G = graph
    k = kVal

    #Create the initial values and find whether it fits
    initGraph()
    numK = getCopNumber()

    return numK
