from railwayroutegenerator import generator
from .helper import compare_route_lists


def test_line():
    routes = generator.generate_from_planpro("line-test.ppxml", output_format="python-objects")
    expected_routes = [("60ES", "60AS")]
    compare_route_lists(routes, expected_routes)


if __name__ == '__main__':
    test_line()
