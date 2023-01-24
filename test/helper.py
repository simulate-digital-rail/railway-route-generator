def _test_single_route(route, expected_route):
    return (
        route.start_signal.name == expected_route[0]
        and route.end_signal.name == expected_route[1]
    )


def compare_route_lists(generated_routes, expected_routes):
    for expected_route in expected_routes:
        found_any = False
        for route in generated_routes:
            found_any = found_any or _test_single_route(route, expected_route)
        assert found_any, "Route " + str(expected_route) + " not found."

    for route in generated_routes:
        found_any = False
        for expected_route in expected_routes:
            found_any = found_any or _test_single_route(route, expected_route)
        assert (
            found_any
        ), f"Route {route.start_signal.name}-{route.end_signal.name} found but was not expected."

    assert len(generated_routes) == len(expected_routes)
