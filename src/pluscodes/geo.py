from dataclasses import dataclass
from types import ClassMethodDescriptorType
from typing import Dict, Tuple


@dataclass(frozen=True)
class Point:
    """A two-dimensional geocoordinate."""

    lat: float
    lon: float

    def latlon(self) -> Tuple[float, float]:
        """Return a Latitude, Longitude (y, x) tuple."""
        return (self.lat, self.lon)

    def lonlat(self) -> Tuple[float, float]:
        """Return a Longitude, Latitude (x, y) tuple."""
        return (self.lon, self.lat)

    def dict(self) -> Dict[str, float]:
        """Point represented as a dictionary."""
        return {"lat": self.lat, "lon": self.lon}


@dataclass(frozen=True)
class Area:
    """
    Boundary box coordinates defining a Plus Code's geographic region.

    Attributes:
        sw: The southwest (low) coordinates.
        ne: The northeast (high) coordinates.
        size: The unpadded code length.
    """

    sw: Point
    ne: Point
    code_length: int

    def center(self) -> Point:
        """The center point of the Plus Code area."""
        lat = round(min((self.sw.lat + self.ne.lat) / 2, 90), 14)
        lon = round(min((self.sw.lon + self.ne.lon) / 2, 180), 14)
        return Point(lat=lat, lon=lon)

    def dict(self) -> Dict[str, Dict[str, float]]:
        """Area as a dict."""
        return {"sw": self.sw.dict(), "ne": self.ne.dict()}

    def tuple(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Return a tuple containing the Plus Ccode, Southwest point and Northeast
        point boundaries
        """
        return (self.sw.latlon(), self.ne.latlon())

    @classmethod
    def from_floats(cls, sw_lat: float, sw_lon: float, ne_lat: float, ne_lon: float):
        """Alternative constructor"""
        sw = Point(lat=round(sw_lat, 14), lon=round(sw_lon, 14))
        ne = Point(lat=round(ne_lat, 14), lon=round(ne_lon, 14))
        return cls(sw=sw, ne=ne)
