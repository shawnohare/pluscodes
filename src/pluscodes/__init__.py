# NOTE: This is a heavily modified version of Google's
# Open Location Code Python implementation.
"""
Convert locations to and from Plus Codes.

Plus Codes are short, 10-11 character codes that can be used instead
of street addresses. The codes can be generated and decoded offline, and use
a reduced character set that minimises the chance of codes including words.

Codes are able to be shortened relative to a nearby location. This means that
in many cases, only four to seven characters of the code are needed.
To recover the original code, the same location is not required, as long as
a nearby location is provided.

Codes represent rectangular areas rather than points, and the longer the
code, the smaller the area. A 10 character code represents a 13.5x13.5
meter area (at the equator. An 11 character code represents approximately
a 2.8x3.5 meter area.

Two encoding algorithms are used. The first 10 characters are pairs of
characters, one for latitude and one for longitude, using base 20. Each pair
reduces the area of the code by a factor of 400. Only even code lengths are
sensible, since an odd-numbered length would have sides in a ratio of 20:1.

At position 11, the algorithm changes so that each character selects one
position from a 4x5 grid. This allows single-character refinements.

Examples:

    Encode a location, default accuracy:
    encode(47.365590, 8.524997)

    Encode a location using one stage of additional refinement:
    encode(47.365590, 8.524997, 11)

    Decode a full code:
    coord = decode(code)
    msg = "Center is {lat}, {lon}".format(lat=coord.latitudeCenter, lon=coord.longitudeCenter)

    Attempt to trim the first characters from a code:
    shorten('8FVC9G8F+6X', 47.5, 8.5)

    Recover the full code from a short code:
    recoverNearest('9G8F+6X', 47.4, 8.6)
    recoverNearest('8F+6X', 47.4, 8.6)
"""
from .code import PlusCode
from .decoder import Decoder
from .encoder import Encoder
from .geo import Area, Point
from .transformer import Transformer
