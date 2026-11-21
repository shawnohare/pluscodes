"""Test that this implementation and the reference match.
"""
import random

import pytest

from pluscodes import Decoder, Encoder
from pluscodes import openlocationcode as olc


# TODO: This just serves as a very basic sanity check. We should port over
# the google test suite as well.
class TestPlusCodeEqualsVendoredCode:
    """Test Whether the Plus Code values values returned from this
    package are the same as those produced by the reference implementation.
    """

    def test_random(self):
        decoder = Decoder()
        encoder = Encoder()
        random.seed(42)

        for _ in range(1000):
            lat = random.uniform(-80, 80)
            lon = random.uniform(-180, 180)
            code = encoder.encode(lat, lon)
            olc_code = olc.encode(lat, lon)

            assert encoder.encode(lat, lon) == olc.encode(lat, lon)

            olc_decoded = olc.decode(code)
            area = decoder.decode(code)
            actual_sw = area.sw.latlon()
            actual_ne = area.ne.latlon()
            expected_sw = olc_decoded.latitudeLo, olc_decoded.longitudeLo
            expected_ne = olc_decoded.latitudeHi, olc_decoded.longitudeHi
            assert actual_sw == expected_sw
            assert actual_ne == expected_ne

    @pytest.mark.parametrize(
        "lat,lon",
        [
            (-90, -180),
            (-90, 0),
            (-90, 180),
            (0, -180),
            (0, 0),
            (0, 180),
            (90, -180),
            (90, 0),
            (90, 180),
        ],
    )
    def test_edges_parameterized(self, lat: float, lon: float):
        """Tests some edge cases that can be problematic. In particular
        the source implementation seems to handle lon = 180 differently
        from lon = -180, likely due to half-open intervalues.
        """
        encoder = Encoder()
        assert encoder.encode(lat, lon) == olc.encode(lat, lon)


@pytest.mark.parametrize(
    "lat,lon,code_length",
    [
        (65.0, -407.7848844, 12),
        (48.853125, 468.3791795, 8),
        (-90, 253.1957942, 6),
        (89.9999999, 531.6863771, 8),
        (95.0, 10.0, 10),
        (-95.0, -190.0, 10),
        (20.0, 540.0, 10),
    ],
)
def test_encode_normalizes_out_of_range_values(lat: float, lon: float, code_length: int):
    assert Encoder(code_length).encode(lat, lon) == olc.encode(lat, lon, code_length)
