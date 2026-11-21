"""Test recovering full codes from short codes."""

import pytest

from pluscodes import openlocationcode as olc
from pluscodes.transformer import Transformer, normalize_lon


@pytest.mark.parametrize(
    "short,lat,lon,expected",
    [
        ("84J9+XG", 59.329394, 18.068712, "9FFW84J9+XG"),
        ("84J9+XGG", 59.329394, 18.068712, "9FFW84J9+XGG"),
        ("FW84J9+XGGC", 59.329394, 18.068712, "9FFW84J9+XGGC"),
        ("PWC3+7VMM", 84.711839, 122.186366, "CQP3PWC3+7VMM"),
        ("H93GF7+26WV", 80.650077, 27.657048, "CGH93GF7+26WV"),
        ("83JC+22XXQC4", 59.329394, 18.068712, "9FFW83JC+22XXQC4"),
        ("W5H36M+9VGM", 28.705625, 180, "72W5H36M+9VGM"),
        ("J8+QQ", 76.053448, 180, "C28222J8+QQ"),
        ("9GX5+VX", 3.931226, 180.854408, "62P29GX5+VX"),
        ("52VR28+HJGC", 73.835836, -180.54247, "C252VR28+HJGC"),
    ],
)
def test_lengthen_keeps_all_digits(short, lat, lon, expected):
    assert Transformer().lenghten(short, (lat, lon)) == expected
    assert olc.recoverNearest(short, lat, lon) == expected


@pytest.mark.parametrize(
    "lon,expected",
    [(180, -180), (-180, -180), (540, -180), (190, -170), (-190, 170), (10, 10)],
)
def test_normalize_lon(lon, expected):
    assert normalize_lon(lon) == expected
