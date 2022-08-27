# pluscodes

A re-implementation of Google's Open Location Code Python package.

## Motivation

The Python implementation of Google's Open Location Code is not
particularly Pythonic nor is it frequently updated. The core code is
in both `openlocationcode` and this package are pure Python with
no dependencies, but the hope is that this implementation will more
readily accept changes.

A longer term goal of this project is to more efficiently handle bulk
Plus Code assignment for offline use.

We vendor the source implementation versioned `v1.0.1` and all that package's
functionality can be accessed via

```python
from pluscodes.vendored import olc
```

# Usage

The main encoder / decoder functions are methods  within the `PlusCode`
class.

```python
from pluscodes import PlusCode

googleplex = PlusCode(37.4223041570954, -122.08410042965134)

print(googleplex.code)
# 849VCWC8+W9

# Get the geocoordinate bounds for the length 10 Plus Code area.
print(googleplex.area)
# Area(sw=Point(lat=37.42225, lon=-122.084125), ne=Point(lat=37.422375, lon=-122.084), code_length=10)

# Decode a Plus Code into a geographic region.
r_googleplex = PlusCode('849VCWC8+W9')

assert googleplex.code == r_googleplex.code
assert googleplex.area == r_googleplex.area
```

# Differences from the reference implementation

This package does not automatically validate or normalize inputs.
For example, it is assumed that all latitude values are in `[-90, 90]`
and all longitude values are  in `[-180, 180]`.
