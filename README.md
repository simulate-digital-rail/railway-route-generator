# Railway Route Generator

This is a small library generating routes (Fahrstraßen) for a given [yaramo](https://github.com/simulate-digital-rail/yaramo) railway topology.

## Installation

Just install it with pip:
```
pip3 install git+https://github.com/arneboockmeyer/railway-route-generator
```

## Usage

```python
from railwayroutegenerator.routegenerator import RouteGenerator

# topology is a yaramo.models.Topology object
RouteGenerator(topology).generate_routes()
print(topology.routes)
```

Further examples can be found in the [demo](https://github.com/simulate-digital-rail/demo) repository.