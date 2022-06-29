import json
from decimal import Decimal


class RunningTrack(object):

    def __init__(self, start_signal, start_edge_uuid):
        self.start_signal = start_signal
        self.edge_uuids = [start_edge_uuid]
        self.end_signal = None

    def duplicate(self):
        new_obj = RunningTrack(self.start_signal, None)
        new_obj.edge_uuids = []
        for edge_uuid in self.edge_uuids:
            new_obj.edge_uuids.append(edge_uuid)
        new_obj.end_signal = self.end_signal
        return new_obj

    def toJSON(self, edge_lengths):
        output_dict = dict()
        output_dict["start_signal"] = self.start_signal.uuid
        output_dict["edges"] = []

        for i in range(0, len(self.edge_uuids)):
            if i == 0:
                edge_uuid = self.edge_uuids[i]
                from_d = 0.0
                to_d = 0.0
                if self.start_signal.wirkrichtung == "in":
                    from_d = self.start_signal.distance
                    to_d = edge_lengths[edge_uuid]
                else:
                    from_d = self.start_signal.distance
                    to_d = 0.0
                output_dict["edges"].append({"edge_uuid": edge_uuid, "from": float(from_d), "to": float(to_d)})
            elif i == len(self.edge_uuids) - 1:
                edge_uuid = self.edge_uuids[i]
                from_d = 0.0
                to_d = 0.0
                if self.end_signal.wirkrichtung == "in":
                    from_d = 0.0
                    to_d = self.end_signal.distance
                else:
                    from_d = edge_lengths[edge_uuid]
                    to_d = self.end_signal.distance
                output_dict["edges"].append({"edge_uuid": edge_uuid, "from": float(from_d), "to": float(to_d)})
                pass
            else:
                edge_uuid = self.edge_uuids[i]
                output_dict["edges"].append({"edge_uuid": edge_uuid, "from": float(0), "to": float(edge_lengths[edge_uuid])})

        output_dict["end_signal"] = self.end_signal.uuid
        return json.dumps(output_dict, sort_keys=True, indent=4)
