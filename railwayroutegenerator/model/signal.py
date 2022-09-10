class Signal(object):

    def __init__(self, uuid):
        self.uuid = uuid
        self.previous_node = None
        self.next_node = None
        self.function = None
        self.distance = 0.0
        self.wirkrichtung = "in"
        self.name = None
