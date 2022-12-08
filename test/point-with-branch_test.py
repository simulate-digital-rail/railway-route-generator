from planpro_importer.reader import PlanProReader

from railwayroutegenerator import generator
from .helper import compare_route_lists


def test_point_with_branch():
    topology = PlanProReader("point-with-branch.ppxml").read_topology_from_plan_pro_file()
    routes = generator.generate_from_topology(topology, output_format="python-objects")
    expected_routes = [("60BS1", "60BS2"), ("60BS1", "60BS3")]
    compare_route_lists(routes, expected_routes)


if __name__ == '__main__':
    test_point_with_branch()
