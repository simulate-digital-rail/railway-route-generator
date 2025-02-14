from planpro_importer import PlanProVersion, import_planpro

from railwayroutegenerator.routegenerator import RouteGenerator

from .helper import compare_route_lists


def test_point_with_branch():
    topology = import_planpro("point-with-branch.ppxml", PlanProVersion.PlanPro19)

    route_generator = RouteGenerator(topology)
    route_generator.generate_routes()

    expected_routes = [("60BS1", "60BS2"), ("60BS1", "60BS3")]
    compare_route_lists(topology.routes, expected_routes)


if __name__ == "__main__":
    test_point_with_branch()
