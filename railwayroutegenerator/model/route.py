import json


class Route(object):

    def __init__(self, start_signal, start_edge):
        self.start_signal = start_signal
        self.edges = [start_edge]
        self.end_signal = None

    def get_length(self):
        length_sum = 0.0
        for edge in self.edges:
            length_sum = length_sum + float(edge.length)
        return length_sum

    def contains_edge(self, _edge):
        for edge in self.edges:
            if edge.uuid == _edge.uuid:
                return True
        return False

    def duplicate(self):
        new_obj = Route(self.start_signal, None)
        new_obj.edges = []
        for edge in self.edges:
            new_obj.edges.append(edge)
        new_obj.end_signal = self.end_signal
        return new_obj

    def to_json(self):
        output_dict = dict()
        output_dict["start_signal"] = self.start_signal.uuid
        output_dict["edges"] = []

        for i in range(0, len(self.edges)):
            edge = self.edges[i]
            from_d = 0.0
            to_d = 0.0

            if i == 0:
                if self.start_signal.wirkrichtung == "in":
                    from_d = self.start_signal.distance
                    to_d = edge.length
                else:
                    from_d = self.start_signal.distance
                    to_d = 0.0
                output_dict["edges"].append({"edge_uuid": edge.uuid, "from": float(from_d), "to": float(to_d)})
            elif i == len(self.edges) - 1:
                if self.end_signal.wirkrichtung == "in":
                    from_d = 0.0
                    to_d = self.end_signal.distance
                else:
                    from_d = edge.length
                    to_d = self.end_signal.distance
                output_dict["edges"].append({"edge_uuid": edge.uuid, "from": float(from_d), "to": float(to_d)})
                pass
            else:
                output_dict["edges"].append({"edge_uuid": edge.uuid, "from": float(0), "to": float(edge.length)})

        output_dict["end_signal"] = self.end_signal.uuid
        return json.dumps(output_dict, sort_keys=True, indent=4)
