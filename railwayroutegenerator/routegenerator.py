from yaramo.model import Edge, Route
from yaramo.signal import SignalDirection, SignalFunction
from yaramo.topology import Topology


class RouteGenerator:
    def __init__(self, topology, max_route_length: int = 20):
        self.topology: Topology = topology
        self.max_route_length: int = max_route_length

    def traverse_edge(
        self, edge: Edge, direction, current_route=None, active_signal=None
    ):
        if current_route is not None:
            for _edge in current_route.edges:
                if _edge.uuid == edge.uuid:
                    # Loop
                    return []
            if len(current_route.edges) > self.max_route_length:
                return []
        routes = []
        signals_on_edge_in_direction = edge.get_signals_with_direction_in_order(
            direction
        )

        if (
            current_route is None
            and active_signal is None
            and len(signals_on_edge_in_direction) == 0
        ):
            return []  # No signals on this edge, so no start
        if current_route is not None:
            current_route.edges.append(edge)
            if edge.maximum_speed is not None and (
                current_route.maximum_speed is None
                or edge.maximum_speed < current_route.maximum_speed
            ):
                current_route.maximum_speed = edge.maximum_speed

        for signal in signals_on_edge_in_direction:
            if active_signal is None:
                # New start signal
                active_signal = signal
                current_route = Route(signal, maximum_speed=edge.maximum_speed)
            elif (
                active_signal.function != signal.function
                or active_signal.function == SignalFunction.Block_Signal
            ):
                # Route ends at signal
                current_route.end_signal = signal
                routes.append(current_route)
                # And start the next route from this signal
                active_signal = signal
                current_route = Route(signal, maximum_speed=edge.maximum_speed)
            else:
                # Next signal is from the same kind, error
                raise ValueError(
                    "The topology contains two Einfahr_Signals or two Ausfahr_Signals in a row"
                )

        next_node = edge.node_b
        if direction == SignalDirection.GEGEN:
            next_node = edge.node_a

        possible_following_edges = next_node.get_possible_followers(edge)
        for possible_following_edge in possible_following_edges:
            if possible_following_edge is None:
                continue
            next_direction = possible_following_edge.get_direction_based_on_start_node(
                next_node
            )
            routes = routes + self.traverse_edge(
                possible_following_edge,
                next_direction,
                current_route.duplicate(),
                active_signal,
            )

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
                if (
                    route.start_signal.uuid == filtered_route.start_signal.uuid
                    and route.end_signal.uuid == filtered_route.end_signal.uuid
                ):
                    if route.get_length() < filtered_route.get_length():
                        filtered_routes.remove(filtered_route)
                    else:
                        should_be_added = False
            if should_be_added:
                filtered_routes.append(route)

        self.topology.routes = {route.uuid: route for route in filtered_routes}
