from planpro_importer.reader import PlanProReader

from railwayroutegenerator.routegenerator import RouteGenerator

from .helper import compare_route_lists


def test_line_multiple_signals():
    topology = PlanProReader(
        "line-test-multiple-signals.ppxml"
    ).read_topology_from_plan_pro_file()

    route_generator = RouteGenerator(topology)
    route_generator.generate_routes()

    expected_routes = [
        ("60ES1", "60AS1"),
        ("60AS1", "60BS1"),
        ("60BS1", "60ES2"),
        ("60ES2", "60AS2"),
        ("60ES3", "60AS3"),
    ]
    compare_route_lists(topology.routes, expected_routes)


if __name__ == "__main__":
    test_line_multiple_signals()
