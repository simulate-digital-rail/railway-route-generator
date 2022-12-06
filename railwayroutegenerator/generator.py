import json
from railwayroutegenerator.routegenerator import RouteGenerator
from planpro_importer.reader import PlanProReader


def print_output(routes, output_format, output_file):
    if output_format == "json":
        if output_file is None:
            return json.dumps([json.loads(route.to_json()) for route in routes], indent=4)
        else:
            with open(output_file, 'w') as f:
                json.dump([json.loads(route.to_json()) for route in routes], f, indent=4)
    if output_format == "python-objects":
        if output_file is not None:
            print("Warning: The output format 'python-object' does not support printing to files.")
        return routes


def generate_from_topology(topology, output_format="json", output_file_name=None):
    route_generator = RouteGenerator(topology)
    routes = route_generator.generate_routes()
    return print_output(routes, output_format, output_file_name)


if __name__ == "__main__":
    topology = PlanProReader("BPD").read_topology_from_plan_pro_file()
    routes = generate_from_topology(topology, output_format="python-objects")
    for route in routes:
        nodes = [edge.node_a.uuid for edge in route.edges] + [edge.node_b.uuid for edge in route.edges]
        print(f"Route from {route.start_signal.function} {route.start_signal.name} to {route.end_signal.function} {route.end_signal.name} via {', '.join(nodes)}")
