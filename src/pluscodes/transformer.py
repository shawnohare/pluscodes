"""Transformations on short codes."""
import re
from typing import Tuple

from .base import Base
from .decoder import Decoder
from .encoder import Encoder
from .geo import Point
from .types import Number
from .validator import Validator


def normalize_lat(lat: float) -> float:
    """
    Clip a latitude into the range -90 to 90.

    Args:
      lat: A latitude in signed decimal degrees.
    """
    return min(90, max(-90, lat))


def normalize_lon(lon: float) -> float:
    """
    Normalize a longitude into the range -180 to 180, not including 180.
    Args:
      longitude: A longitude in signed decimal degrees.
    """
    if lon < -180:
        while lon < -180:
            lon += 360
    elif lon > 180:
        while lon >= 180:
            lon -= 360
    return lon


class Transformer(Base):
    """Performs transformations on Plus Codes."""

    validator = Validator()
    encoder = Encoder()
    decoder = Decoder()

    def lenghten(self, code: str, ref: Point | Tuple[Number, Number]) -> str:
        """
        Recover the nearest matching code to a specified location.
        Given a short code of between four and seven characters, this recovers
        the nearest matching full code to the specified location.

        Args:
            code: A valid OLC character sequence.
            ref: Reference geocoordinate containing lat, lon values used to find
               the nearest matching full Plus Code.

        Returns:
          The nearest full Plus Code to the reference location that matches
          the short code. If the passed code was not a valid short code, but was a
          valid full code, it is returned with proper capitalization but otherwise
          unchanged.
        """
        code = code.upper()
        # if code is a valid full code, return it properly capitalized
        if self.validator.is_full(code):
            return code.upper()
        if not self.validator.is_short(code):
            raise ValueError("Passed short code is not valid - " + str(code))

        # Ensure that latitude and longitude are valid.
        # Clean up the passed code.
        # Compute the number of digits we need to recover.
        paddingLength = self.SEP_POSITION - code.find(self.SEP)

        # The resolution (height and width) of the padded area in degrees.
        resolution = pow(20, 2 - (paddingLength / 2))
        # Distance from the center to an edge (in degrees).
        halfResolution = resolution / 2.0

        # Use the reference location to pad the supplied short code and decode it.
        if isinstance(ref, tuple):
            ref = Point(*ref)

        area = self.decoder.decode(
            self.encoder.encode(ref.lat, ref.lon)[0:paddingLength] + code
        )

        # How many degrees latitude is the code from the reference? If it is more
        # than half the resolution, we need to move it north or south but keep it
        # within -90 to 90 degrees.
        c_lat, c_lon = area.center().latlon()
        if ref.lat + halfResolution < c_lat and c_lat - resolution >= -self.MAX_LAT:
            # If the proposed code is more than half a cell north of the reference location,
            # it's too far, and the best match will be one cell south.
            c_lat -= resolution
        elif ref.lat - halfResolution > c_lat and c_lat + resolution <= self.MAX_LAT:
            # If the proposed code is more than half a cell south of the reference location,
            # it's too far, and the best match will be one cell north.
            c_lat += resolution

        # Adjust longitude if necessary.
        if ref.lon + halfResolution < c_lon:
            c_lon -= resolution
        elif ref.lon - halfResolution > c_lon:
            c_lon += resolution

        # return self.encoder.encode(c_lat, c_lon, codeArea.code_length)
        return self.encoder.encode(c_lat, c_lon)

    def shorten(self, code, ref: Point | Tuple[Number, Number]) -> str:
        """
        Remove characters from the start of an OLC code.
        This uses a reference location to determine how many initial characters
        can be removed from the OLC code. The number of characters that can be
        removed depends on the distance between the code center and the reference
        location.
        The minimum number of characters that will be removed is four. If more than
        four characters can be removed, the additional characters will be replaced
        with the padding character. At most eight characters will be removed.
        The reference location must be within 50% of the maximum range. This ensures
        that the shortened code will be able to be recovered using slightly different
        locations.
        Args:
          code: A full, valid code to shorten.
          latitude: A latitude, in signed decimal degrees, to use as the reference
              point.
          longitude: A longitude, in signed decimal degrees, to use as the reference
              point.
        Returns:
          Either the original code, if the reference location was not close enough,
          or the .
        """
        if not self.validator.is_full(code):
            raise ValueError(f"Passed code is not valid and full: {code=}")
        if self.PADDING_CHAR in code:
            raise ValueError(f"Cannot shorten padded codes: {code=}")

        if isinstance(ref, tuple):
            ref = Point(*ref)

        code = code.upper()
        area = self.decoder.decode(code)

        if len(re.sub("[+0]", "", code)) < self.MIN_TRIMMABLE_CODE_LEN:
            raise ValueError(
                f"Code length must be at least {self.MIN_TRIMMABLE_CODE_LEN}"
            )

        # Ensure that latitude and longitude are valid.
        # How close are the latitude and longitude to the code center.
        c_lat, c_lon = area.center().latlon()
        coderange = max(abs(c_lat - ref.lat), abs(c_lon - ref.lon))
        for i in range(len(self.PAIR_RESOLUTIONS) - 2, 0, -1):
            # Check if we're close enough to shorten. The range must be less than 1/2
            # the resolution to shorten at all, and we want to allow some safety, so
            # use 0.3 instead of 0.5 as a multiplier.
            if coderange < (self.PAIR_RESOLUTIONS[i] * 0.3):
                # Trim it.
                return code[(i + 1) * 2 :]
        return code
