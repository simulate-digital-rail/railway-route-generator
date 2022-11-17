from railwayroutegenerator import generator


def test_simple_point():
    routes = generator.generate_from_planpro("simple-point-test.ppxml", output_format="python-objects")
    assert len(routes) == 1
    assert routes[0].start_signal.name == "60ES"
    assert routes[0].end_signal.name == "60AS"


if __name__ == '__main__':
    test_simple_point()
