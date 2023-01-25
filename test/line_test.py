from planpro_importer.reader import PlanProReader
from railwayroutegenerator.routegenerator import RouteGenerator

from .helper import compare_route_lists


def test_line():
    topology = PlanProReader("line-test.ppxml").read_topology_from_plan_pro_file()

    route_generator = RouteGenerator(topology)
    route_generator.generate_routes()

    expected_routes = [("60ES", "60AS")]
    compare_route_lists(topology.routes, expected_routes)


if __name__ == "__main__":
    test_line()
