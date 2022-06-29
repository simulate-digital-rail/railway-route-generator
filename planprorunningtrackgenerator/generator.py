import planpromodel
import json
from .model.node import Node
from .model.signal import Signal
from .model.running_track import RunningTrack


def read_topology_from_container(container):
    nodes = dict()
    edges = dict()
    edge_uuids_by_nodes = dict()
    edge_lengths = dict()

    for top_knoten in container.TOP_Knoten:
        top_knoten_uuid = top_knoten.Identitaet.Wert
        node_obj = Node(top_knoten_uuid)
        nodes[top_knoten_uuid] = node_obj

    for top_kante in container.TOP_Kante:
        top_kante_uuid = top_kante.Identitaet.Wert
        node_a = nodes[top_kante.ID_TOP_Knoten_A.Wert]
        node_b = nodes[top_kante.ID_TOP_Knoten_B.Wert]

        # Anschluss A
        anschluss_a = top_kante.TOP_Kante_Allg.TOP_Anschluss_A.Wert
        if anschluss_a == "Ende" or anschluss_a == "Spitze":
            node_a.set_connection_head(node_b)
        elif anschluss_a == "Links":
            node_a.set_connection_left(node_b)
        elif anschluss_a == "Rechts":
            node_a.set_connection_right(node_b)

        # Anschluss B
        anschluss_b = top_kante.TOP_Kante_Allg.TOP_Anschluss_B.Wert
        if anschluss_b.startswith("Ende") or anschluss_b == "Spitze":
            node_b.set_connection_head(node_a)
        elif anschluss_b == "Links":
            node_b.set_connection_left(node_a)
        elif anschluss_b == "Rechts":
            node_b.set_connection_right(node_a)

        edges[top_kante_uuid] = (node_a, node_b)
        edge_uuids_by_nodes[node_a.uuid + ":" + node_b.uuid] = top_kante_uuid
        edge_lengths[top_kante_uuid] = top_kante.TOP_Kante_Allg.TOP_Laenge.Wert

    return nodes, edges, edge_uuids_by_nodes, edge_lengths


def read_signals_from_container(container, nodes, edges):
    signals = []
    for signal in container.Signal:
        signal_uuid = signal.Identitaet.Wert
        signal_obj = Signal(signal_uuid)

        if signal.Signal_Real.Signal_Real_Aktiv is not None:
            # if len(signal.Punkt_Objekt_TOP_Kante) == 1:  # If greater, no real signal with lights
            signal_obj.function = signal.Signal_Real.Signal_Real_Aktiv.Signal_Funktion.Wert
            top_kante_id = signal.Punkt_Objekt_TOP_Kante[0].ID_TOP_Kante.Wert
            signal_obj.wirkrichtung = signal.Punkt_Objekt_TOP_Kante[0].Wirkrichtung.Wert
            signal_obj.distance = signal.Punkt_Objekt_TOP_Kante[0].Abstand.Wert
            node_tuple = edges[top_kante_id]

            if signal_obj.wirkrichtung == "in":
                signal_obj.previous_node = node_tuple[0]
                signal_obj.next_node = node_tuple[1]
            else:
                signal_obj.previous_node = node_tuple[1]
                signal_obj.next_node = node_tuple[0]
            signals.append(signal_obj)
    return signals


def read_topology(input_planpro_file):
    nodes = dict()
    edges = dict()
    edge_uuids_by_nodes = dict()
    edge_lengths = dict()
    signals = []

    root_object = planpromodel.parse(input_planpro_file+".ppxml", silence=True)
    number_of_fachdaten = len(root_object.LST_Planung.Fachdaten.Ausgabe_Fachdaten)

    for id_of_fachdaten in range(0, number_of_fachdaten):
        container = root_object.LST_Planung.Fachdaten.Ausgabe_Fachdaten[id_of_fachdaten].LST_Zustand_Ziel.Container
        nodes_con, edges_con, edge_uuids_by_nodes_con, edge_lengths_con = read_topology_from_container(container)
        nodes.update(nodes_con)
        edges.update(edges_con)
        edge_uuids_by_nodes.update(edge_uuids_by_nodes_con)
        edge_lengths.update(edge_lengths_con)

    for id_of_fachdaten in range(0, number_of_fachdaten):
        container = root_object.LST_Planung.Fachdaten.Ausgabe_Fachdaten[id_of_fachdaten].LST_Zustand_Ziel.Container
        signals = signals + read_signals_from_container(container, nodes, edges)

    return nodes, edges, edge_uuids_by_nodes, edge_lengths, signals


def get_edge_uuid_by_nodes(edge_uuids_by_nodes, node_a, node_b):
    uuid_connected_first_way = node_a.uuid + ":" + node_b.uuid
    uuid_connected_second_way = node_b.uuid + ":" + node_a.uuid

    if uuid_connected_first_way in edge_uuids_by_nodes:
        return edge_uuids_by_nodes[uuid_connected_first_way]
    elif uuid_connected_second_way in edge_uuids_by_nodes:
        return edge_uuids_by_nodes[uuid_connected_second_way]
    return None


def get_signals_at_edge(current_node, next_node, signals):
    result = []
    for signal in signals:
        if signal.is_signal_on_edge(current_node, next_node):
            result.append(signal)
    return result


def dfs(current_node, previous_node, current_track, edge_uuids_by_nodes, signals):
    next_nodes = current_node.get_possible_followers(previous_node)
    if next_nodes is None or len(next_nodes) == 0:
        return []

    found_tracks = []
    for next_node in next_nodes:
        edge_uuid = get_edge_uuid_by_nodes(edge_uuids_by_nodes, current_node, next_node)
        if edge_uuid is None:
            print("Bad error, edge not found, datstructure broken.")
        else:
            track_with_edge = current_track.duplicate()
            track_with_edge.edge_uuids.append(edge_uuid)
            for signal in get_signals_at_edge(current_node, next_node, signals):
                if signal.function == "Ausfahr_Signal": # TODO: Whats about single edges with multiple Einfahr und Ausfahr signals?
                    closed_track = track_with_edge.duplicate()
                    closed_track.end_signal = signal
                    found_tracks.append(closed_track)
            # TODO: Whats about multiple Ausfahr signals in a row on different tracks? Should it only effect the first
            # one? Means: If a Ausfahr Signal is found before, no further DFS on that path.
            found_tracks = found_tracks + dfs(next_node, current_node, track_with_edge, edge_uuids_by_nodes, signals)
    return found_tracks


def generate_running_tracks(edge_uuids_by_nodes, signals):
    running_tracks = []
    for signal in signals:
        if signal.function == "Einfahr_Signal":
            running_track = RunningTrack(signal, get_edge_uuid_by_nodes(edge_uuids_by_nodes, signal.previous_node, signal.next_node))
            next_node = signal.next_node
            running_tracks = running_tracks + dfs(next_node, signal.previous_node, running_track, edge_uuids_by_nodes, signals)
    return running_tracks


def print_output(running_tracks, edge_lengths, output_format, output_file):
    if output_format == "json":
        if output_file is None:
            return json.dumps([json.loads(running_track.toJSON(edge_lengths)) for running_track in running_tracks], indent=4)
        else:
            with open(output_file, 'w') as f:
                json.dump([json.loads(running_track.toJSON(edge_lengths)) for running_track in running_tracks], f, indent=4)


def generate(input_planpro_file, output_format="json"):
    nodes, edges, edge_uuids_by_nodes, edge_lengths, signals = read_topology(input_planpro_file)
    running_tracks = generate_running_tracks(edge_uuids_by_nodes, signals)
    return print_output(running_tracks, edge_lengths, output_format, None)


def generate_to_file(input_planpro_file, output_file, output_format="json"):
    nodes, edges, edge_uuids_by_nodes, edge_lengths, signals = read_topology(input_planpro_file)
    running_tracks = generate_running_tracks(edge_uuids_by_nodes, signals)
    print_output(running_tracks, edge_lengths, output_format, output_file)
