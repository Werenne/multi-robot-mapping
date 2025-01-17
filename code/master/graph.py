
import heapq  
from utils import center2xy

#---------------
class Graph():
    
    def __init__(self, map_orientation, map_type2edges):
        self.map_orientation = map_orientation
        self.map_type2edges = map_type2edges
        self._edges = {}
        self.nodes = {}

        self.new_node((0,0), 0, 7)
        self.new_node((0,40), 0, 0)
        self.new_edge((0,0), 0, (0,40), 2, 40)
    
    #-------
    @property
    def edges(self):
        return [edge.nodes for key, edge in self._edges.items()]

    #-------
    def is_node(self, position):
        return self.nodes.get(position) != None

    #-------
    def is_edge(self, position_a, position_b):
        key = Edge.unique_key(position_a, position_b)
        return self._edges.get(key) != None

    #-------
    def get_node(self, position):
        assert self.is_node(position)
        return self.nodes[position]

    #-------
    def new_node(self, position, orientation, type_intersection):
        if not self.is_node(position):
            self.nodes[position] = Node(position, orientation,
                    type_intersection, self.map_orientation, self.map_type2edges)
        return self

    #-------
    def new_edge(self, position_a, orientation_a, position_b, orientation_b,
            weight):
        if self.is_edge(position_a, position_b):
            return
        assert self.is_node(position_a) and self.is_node(position_b)
        node_a = self.get_node(position_a)
        node_b = self.get_node(position_b)
        edge = Edge(node_a, node_b, weight)
        node_a.connect(edge, orientation_a)
        node_b.connect(edge, orientation_b)
        self._edges[edge.__str__()] = edge

    #-------     
    def reset(self):
        for position, node in self.nodes.items():
            self.nodes[position] = node.reset()
        return self



#---------------
class Node():
    
    def __init__(self, position, orientation, type_intersection, map_orientation,
            map_type2edges):
        self._position = position
        self._visited = False
        self._parent = None
        self._cost = float('Inf') 
        self._type_intersection = type_intersection
        self.edges = {}
        self.map_orientation = map_orientation
        self.map_type2edges = map_type2edges
        self.init_edges(orientation, type_intersection)
    
    #-------
    @property
    def position(self):
        return self._position

    #------- 
    @property
    def visited(self):
        return self._visited

    #-------
    @visited.setter
    def visited(self, visited):
        self._visited = visited

    #-------
    @property
    def parent(self):
        return self._parent

    #-------
    @property
    def type_intersection(self):
        return self._type_intersection

    #-------
    @property
    def parent_to_son_orientation(self):
        for orientation, edge in self.edges.items():
            temp = edge.connected_to(self.position)
            if self._parent != None and temp.position == self._parent.position:
                return orientation
        assert False

    #-------
    @parent.setter
    def parent(self, parent):
        self._parent = parent

    #-------
    @property
    def cost(self):
        return self._cost

    #-------
    @cost.setter
    def cost(self, cost):
        self._cost = cost

    #-------   
    @property
    def neighbors(self):
        neighbors = []
        for _, edge in self.edges.items():
            if edge != None:  
                neighbors.append((edge.connected_to(self.position), edge.weight))
        return neighbors

    #-------   
    @property
    def unexplored_orientations(self):
        unexplored = []
        for orientation, edge in self.edges.items():
            if edge == None:  
                unexplored.append(orientation)
        return unexplored

    #-------   
    @property
    def explored_orientations(self):
        explored = []
        for orientation, edge in self.edges.items():
            if not edge is None:  
                explored.append(orientation)
        return explored 
    
    #-------
    def get_neighbor(self, orien):
        unexplored = []
        for orientation, edge in self.edges.items():
            if orien == orientation and (not edge is None) :  
                return edge.connected_to(self._position)
        return None

    #-------
    def __lt__(self, other):
        return self.position < other.position

    #-------
    def init_edges(self, orientation, type_intersection):
        self.make_edges(type_intersection).rotate_axis(orientation)

    #-------
    def make_edges(self, type_intersection):
        """ 
        Edges are dictionnary: 
               <key,value> = <orientation of edge, edge object>
        """
        keys = self.map_type2edges[type_intersection]
        keys = [self.map_orientation[k] for k in keys]
        for key in keys:
            self.edges[key] = None  
        return self

    #-------
    def rotate_axis(self, orientation):
        keys = self.edges.keys()  # Orientations of edges
        if orientation == self.map_orientation['N']:
            rotated_keys = keys
        elif orientation == self.map_orientation['E']:
            rotated_keys = list(map(lambda x: (x+1)%4, keys))
        elif orientation == self.map_orientation['S']:
            rotated_keys = list(map(lambda x: (x+2)%4, keys))
        elif orientation == self.map_orientation['W']:
            rotated_keys = list(map(lambda x: (x-1)%4, keys))
        temp = {}
        for old_key, new_key in zip(keys, rotated_keys):
            temp[new_key] = self.edges[old_key]
        self.edges = temp

    #-------
    def connect(self, edge, orientation):
        self.edges[orientation] = edge

    #-------
    def reset(self):
        self._visited = False
        self._parent = None
        self._cost = float('Inf')
        return self


#---------------
class Edge():
    
    def __init__(self, a, b, weight):
        self._weight = float(weight)
        self.a = a  # Node part of edge
        self.b = b  # Other node part of edge

    #-------
    @staticmethod
    def unique_key(position_a, position_b):
        def is_a_before_b(pos_a, pos_b):
            if pos_a[0] < pos_b[0]:
                return True
            elif pos_a[0] < pos_b[0]:
                return False
            elif pos_a[1] < pos_b[1]:
                return True
            return False

        if is_a_before_b(position_a, position_b):
            return str(position_a) + ";" + str(position_b)
        else:
            return str(position_b) + ";" + str(position_a)

    #-------
    def __str__(self): 
        return Edge.unique_key(self.a.position, self.b.position)

    #-------
    @property
    def weight(self):
        return self._weight

    #-------
    @property
    def nodes(self):
        return (self.a.position, self.b.position)

    #-------
    def connected_to(self, position):
        if self.a.position == position:
            return self.b
        if self.b.position == position:
            return self.a
        return None 































