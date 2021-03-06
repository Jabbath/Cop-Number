# k-FIXED COP NUMBER
This is a python implementation of the algorithm described in The Game of Cops and Robbers on Graphs by Anthony Bonato to
solve k-FIXED COP NUMBER. The time complexity of the algorithm is O(n^{3k + 3}). This implementation is very slow for k 
greater than about 5 for even moderately sized graphs with 30 - 40 vertices. Currently, input graphs are treated as reflexive.
If they are not reflexive, then self edges are added.

## Usage
First, install the code from pip or the git repo:
```
pip install cop-number
```
Then, use a graph and a k with the `copk` function of `cop`. The function will return `True` if the cop number is greater
than k, and `False` otherwise. See the example below.

```python
import networkx as nx
from cop_number.cop import copk

G = nx.petersen_graph()

result1 = copk(G, 1)
#True

result2 = copk(G, 2)
#True

result3 = copk(G, 3)
#False
```

A function that automates the finding of cop number through `copk` has also been implemented.
It can be used as follows:

```python
import networkx as nx
from cop_number.cop import cop_num

G = nx.petersen_graph()

result = cop_num(G)
#3
```

## Contributing
If you feel that you have something useful to add, feel free to submit a pull request.

## License
Licensed under the MIT license. See license.txt.
