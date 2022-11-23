from railwayroutegenerator import generator
from .helper import compare_route_lists


def test_simple_point():
    routes = generator.generate_from_planpro("simple-point-test.ppxml", output_format="python-objects")
    expected_routes = [("60ES", "60AS")]
    compare_route_lists(routes, expected_routes)


if __name__ == '__main__':
    test_simple_point()
