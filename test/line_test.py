from railwayroutegenerator import generator


def test_line():
    routes = generator.generate_from_planpro("line-test.ppxml", output_format="python-objects")
    assert len(routes) == 1


if __name__ == '__main__':
    test_line()
