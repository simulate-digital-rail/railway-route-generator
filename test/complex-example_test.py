from planpro_importer.reader import PlanProReader
from railwayroutegenerator.routegenerator import RouteGenerator

from .helper import compare_route_lists


def test_complex_example():
    topology = PlanProReader("complex-example.ppxml").read_topology_from_plan_pro_file()

    route_generator = RouteGenerator(topology)
    route_generator.generate_routes()

    expected_routes = [
        ("60BS1", "60BS2"),
        ("60BS2", "60BS3"),
        ("60BS1", "60ES1"),
        ("60ES1", "60AS1"),
        ("60ES1", "60AS2"),
        ("60AS1", "60BS3"),
        ("60AS2", "60BS3"),
        ("60BS4", "60BS5"),
        ("60BS5", "60BS6"),
        ("60BS6", "60BS7"),
        ("60BS4", "60ES2"),
        ("60ES2", "60AS3"),
        ("60ES2", "60AS4"),
        ("60AS3", "60BS7"),
        ("60AS4", "60BS7"),
    ]
    compare_route_lists(topology.routes, expected_routes)


if __name__ == "__main__":
    test_complex_example()
