

class Signal(object):

    def __init__(self, uuid):
        self.uuid = uuid
        self.previous_node = None
        self.next_node = None
        self.function = None
        self.distance = 0.0
        self.wirkrichtung = "in"

    def is_signal_on_edge(self, previous_node, next_node):
        return self.previous_node.uuid == previous_node.uuid and self.next_node.uuid == next_node.uuid
