from yaramo.model import Route
from yaramo.signal import SignalDirection, SignalFunction


class RouteGenerator(object):

    def __init__(self, topology):
        self.topology = topology

    def traverse_edge(self, edge, direction, current_route=None, active_signal=None):
        routes = []
        signals_on_edge_in_direction = edge.get_signals_with_direction_in_order(direction)

        if current_route is None and active_signal is None and len(signals_on_edge_in_direction) == 0:
            return []  # No signals on this edge, so no start
        if current_route is not None:
            current_route.edges.append(edge)

        for signal in signals_on_edge_in_direction:
            if active_signal is None:
                # New start signal
                active_signal = signal
                current_route = Route(signal)
            elif active_signal.function != signal.function or active_signal.function == SignalFunction.Block_Signal:
                # Route ends at signal
                current_route.end_signal = signal
                routes.append(current_route)
                # And start the next route from this signal
                active_signal = signal
                current_route = Route(signal)

        next_node = edge.node_b
        previous_node = edge.node_a
        if direction == SignalDirection.GEGEN:
            next_node = edge.node_a
            previous_node = edge.node_b

        possible_followers = next_node.get_possible_followers(previous_node)
        for possible_follower in possible_followers:
            next_edge = self.topology.get_edge_by_nodes(next_node, possible_follower)
            next_direction = next_edge.get_direction_based_on_nodes(next_node, possible_follower)
            routes = routes + self.traverse_edge(next_edge, next_direction, current_route.duplicate(), active_signal)

        return routes

    def generate_routes(self):
        routes = []
        for edge_uuid in self.topology.edges:
            edge = self.topology.edges[edge_uuid]
            routes = routes + self.traverse_edge(edge, SignalDirection.IN)
            routes = routes + self.traverse_edge(edge, SignalDirection.GEGEN)

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
