class Edge(object):

    def __init__(self, uuid, node_a, node_b, length):
        self.uuid = uuid
        self.node_a = node_a
        self.node_b = node_b
        self.signals = []
        self.length = length

    def get_direction_based_on_nodes(self, node_a, node_b):
        if self.node_a.uuid == node_a.uuid and self.node_b.uuid == node_b.uuid:
            return "in"
        elif self.node_a.uuid == node_b.uuid and self.node_b.uuid == node_a.uuid:
            return "gegen"
        return None

    def get_signals_with_direction_in_order(self, direction):
        result = []
        for signal in self.signals:
            if signal.wirkrichtung == direction:
                result.append(signal)
        result.sort(key=lambda x: x.distance, reverse=(direction == "gegen"))
        return result
