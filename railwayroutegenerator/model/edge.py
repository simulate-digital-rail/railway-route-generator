class Edge(object):

    def __init__(self, uuid, node_a, node_b, length):
        self.uuid = uuid
        self.node_a = node_a
        self.node_b = node_b
        self.signals = []
        self.length = length
