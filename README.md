# k-FIXED COP NUMBER
This is a python implementation of the algorithm described in The Game of Cops and Robbers on Graphs by Anthony Bonato to
solve k-FIXED COP NUMBER. The time complexity of the algorithm is O(n^{3k + 3}). This implementation is very slow for k 
greater than about 5 for even moderately sized graphs with 30 - 40 vertices. Currently, input graphs are treated as reflexive.
If they are not reflexive, then self edges are added.

## Usage
First, import the code:
```
import copk from cop
```
Then, use a graph and a k to check for can be fed to copk. The function will return `True` if the cop number is greater
than k, and `False` otherwise. See the example below.

```python
import networkx as nx
import copk from cop

G = nx.petersen_graph()

result1 = copk(G, 1)
#True

result2 = copk(G, 2)
#True

result3 = copk(G, 3)
#False
```
## Contributing
If you feel that you have something useful to add, feel free to submit a pull request.

## License
Licensed under the MIT license. See license.txt.
