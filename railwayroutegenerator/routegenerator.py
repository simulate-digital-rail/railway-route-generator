from .model import Route


class RouteGenerator(object):

    def __init__(self, topology):
        self.topology = topology

    def dfs(self, current_node, previous_node, current_route):
        next_nodes = current_node.get_possible_followers(previous_node)
        if next_nodes is None or len(next_nodes) == 0:
            return []

        found_routes = []
        for next_node in next_nodes:
            edge = self.topology.get_edge_by_nodes(current_node, next_node)
            if edge is None:
                print("Bad error, edge not found, datastructure broken.")
            else:
                route_with_edge = current_route.duplicate()
                route_with_edge.edges.append(edge)
                for signal in edge.signals:
                    if signal.function == "Ausfahr_Signal" or signal.function == "Block_Signal":  # TODO: Whats about single edges with multiple Einfahr und Ausfahr signals?
                        closed_track = route_with_edge.duplicate()
                        closed_track.end_signal = signal
                        found_routes.append(closed_track)
                # TODO: Whats about multiple Ausfahr signals in a row on different tracks? Should it only effect the first
                # one? Means: If a Ausfahr Signal is found before, no further DFS on that path.
                found_routes = found_routes + self.dfs(next_node, current_node, route_with_edge)
        return found_routes

    def generate_routes(self):
        routes = []
        for signal_uuid in self.topology.signals:
            signal = self.topology.signals[signal_uuid]
            if signal.function == "Einfahr_Signal" or signal.function == "Block_Signal":
                route = Route(signal, self.topology.get_edge_by_nodes(signal.previous_node, signal.next_node))
                next_node = signal.next_node
                routes = routes + self.dfs(next_node, signal.previous_node, route)

        # Filter duplicates
        filtered_routes = []
        for route in routes:
            should_be_added = True
            for filtered_route in filtered_routes:
                if route.start_signal.uuid == filtered_route.start_signal.uuid and \
                   route.end_signal.uuid == filtered_route.end_signal.uuid:
                    if route.get_length() < filtered_route.get_length():
                        filtered_routes.remove(filtered_route)
                    else:
                        should_be_added = False
            if should_be_added:
                filtered_routes.append(route)

        return filtered_routes
