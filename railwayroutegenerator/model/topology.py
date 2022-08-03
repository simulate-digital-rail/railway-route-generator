class Topology(object):

    def __init__(self):
        self.nodes = dict()
        self.edges = dict()
        self.signals = dict()

    def add_node(self, node):
        self.nodes[node.uuid] = node

    def add_edge(self, edge):
        self.edges[edge.uuid] = edge

    def add_signal(self, signal):
        self.signals[signal.uuid] = signal

    def get_edge_by_nodes(self, node_a, node_b):
        for edge_uuid in self.edges:
            edge = self.edges[edge_uuid]
            if edge.node_a.uuid == node_a.uuid and edge.node_b.uuid == node_b.uuid or \
               edge.node_a.uuid == node_b.uuid and edge.node_b.uuid == node_a.uuid:
                return edge
        return None

