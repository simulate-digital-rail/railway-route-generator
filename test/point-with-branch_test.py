from railwayroutegenerator import generator
from .helper import compare_route_lists


def test_point_with_branch():
    routes = generator.generate_from_planpro("point-with-branch.ppxml", output_format="python-objects")
    expected_routes = [("60BS1", "60BS2"), ("60BS1", "60BS3")]
    compare_route_lists(routes, expected_routes)


if __name__ == '__main__':
    test_point_with_branch()
