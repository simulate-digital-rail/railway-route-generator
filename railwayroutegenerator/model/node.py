class Node(object):
    # A node represents a top node, its connections are top edges

    def __init__(self, uuid):
        self.uuid = uuid
        self.connected_on_head = None
        self.connected_on_left = None
        self.connected_on_right = None
        self.connected_nodes = []

    def set_connection_head(self, node):
        self.connected_on_head = node
        self.connected_nodes.append(node)

    def set_connection_left(self, node):
        self.connected_on_left = node
        self.connected_nodes.append(node)

    def set_connection_right(self, node):
        self.connected_on_right = node
        self.connected_nodes.append(node)

    def get_possible_followers(self, source):
        # Node is end. If the source is null (no node) the only connected node is a possible follower.
        # Otherwise return an empty list to indicate the end.
        if len(self.connected_nodes) == 1:
            if source is None:
                return self.connected_nodes
            else:
                return []

        # Otherwise its a point
        if source is None:
            return [self.connected_on_head, self.connected_on_left, self.connected_on_right]
        if source.uuid == self.connected_on_head.uuid:  # Comes from head
            return [self.connected_on_left, self.connected_on_right]
        else:
            return [self.connected_on_head]
