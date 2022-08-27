# pluscodes

An implementation of Google's Open Location Code algorithm forked from
the `openlocationcode==1.0.1` package.

## Motivation

The Python implementation of Google's Open Location Code is not particularly
Pythonic with respect to its naming conventions. The core code is in both
`openlocationcode` and this package are pure Python with no dependencies
outside of the standard library.

We hope to presents geocoordinates using a more consistent API. A longer term goal
to more efficiently handle bulk Plus Code assignments and further more
readily enable Plus Code lookup and categorization.

# Installation

This package is available in PyPi, so simply

```bash
pip install pluscodes
```


# Usage

The `PlusCode` constructor provides the main entry point for generating
the string Plus Code (encoding) and geographic area boundary ("decoding").

```python
from pluscodes import PlusCode, Area, Point

googleplex = PlusCode(37.4223041570954, -122.08410042965134)

assert googleplex.code == '849VCWC8+W9'

# Get the geocoordinate bounds for the length 10 Plus Code area.
assert googleplex.area == Area(
    sw=Point(lat=37.42225, lon=-122.084125),
    ne=Point(lat=37.422375, lon=-122.084),
)

# Decode a Plus Code into a geographic region.
r_googleplex = PlusCode('849VCWC8+W9')

assert googleplex.code == r_googleplex.code
assert googleplex.area == r_googleplex.area
```

This package also provides the original `openlocationcode==1.0.1` package
as a subpackage for use-cases that wish to adhere to openlocationcode's
API.


```python
import pluscodes
from pluscodes import openlocationcode

expected_code = '6FG22222+22'
plus = pluscodes.encode(0.0, 0.0)
olc = openlocationcode.encode(0.0, 0.0)

assert (plus == expected_code) and (olc == expected_code)

print(openlocationcode.decode('6FG22222+22'))
# [0.0, 0.0, 0.000125, 0.000125, 6.25e-05, 6.25e-05, 10]

print(pluscodes.decode('6FG22222+22'))
# Area(sw=Point(lat=0.0, lon=0.0), ne=Point(lat=0.000125, lon=0.000125))
```


# Differences from openlocationcode

This package does not automatically validate or normalize inputs.
For example, it is assumed that all latitude values are in `[-90, 90]`
and all longitude values are  in `[-180, 180]`.

Moreover, the encoding and decoding APIs are combined in the PlusCode
class, with the decoding API producing a simple dataclass consisting of two
Point instances.
