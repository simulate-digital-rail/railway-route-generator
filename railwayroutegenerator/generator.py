import json
from .planproreader import PlanProReader
from .routegenerator import RouteGenerator


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


def generate_from_planpro(planpro_file, output_format="json", output_file_name=None):
    pp_reader = PlanProReader(planpro_file)
    topology = pp_reader.read_topology_from_plan_pro_file()
    return generate_from_topology(topology, output_format, output_file_name)


def generate_to_file(input_planpro_file, output_file, output_format="json"):
    generate_from_planpro(input_planpro_file, output_format, output_file)


def generate(input_planpro_file, output_format="json"):
    return generate_from_planpro(input_planpro_file, output_format)
