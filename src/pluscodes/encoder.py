import math
import re
from dataclasses import dataclass
from typing import Dict, Tuple

from .base import Base
from .types import Number


class Encoder(Base):
    """
    Create Plus Codes of a specified length from geocoordinate inputs.

    By default, Plus Codes corresponding to 13m x 13m (at equator) regions
    are computed.

    """

    def __init__(self, code_length: int = 10):
        # Validate code_length.
        if not (2 <= code_length <= self.MAX_CODE_LENGTH) or (
            code_length < self.PAIR_CODE_LENGTH and code_length % 2 == 1
        ):
            raise ValueError(f"Invalid code length: {code_length=}")

        self.code_length = code_length

        # Compute the latitude precision value for a given code length.
        # Lengths <= 10 have the same precision for latitude and longitude, but
        # lengths > 10 have different precisions due to the grid method having
        # fewer columns than rows.
        if code_length <= 10:
            self._lat_precision = pow(20, math.floor((code_length / -2) + 2))
        else:
            self._lat_precision = pow(20, -3) / pow(self.GRID_ROWS, code_length - 10)

    def encode(self, latitude: Number, longitude: Number) -> str:
        """
        Encode a location into an Plus Code.

        Produces a code of the specified length, or the default length if no length
        is provided.
        The length determines the accuracy of the code. The default length is
        10 characters, returning a code of approximately 13.5x13.5 meters. Longer
        codes represent smaller areas, but lengths > 14 are sub-centimetre and so
        11 or 12 are probably the limit of useful codes.
        Args:
          latitude: A latitude in signed decimal degrees. Will be clipped to the
              range -90 to 90.
          longitude: A longitude in signed decimal degrees. Will be normalised to
              the range -180 to 180.
          code_length: The number of significant digits in the output code, not
              including any separator characters.
        """
        # TODO: Is there a way to easily compute the boundary while encoding
        # instead of performing a code / decode op?

        # Latitude 90 needs to be adjusted to be just less, so the returned code
        # can also be decoded.
        if latitude == 90:
            latitude = latitude - self._lat_precision

        # The source implementation maps 180 -> -180 via the function
        # that normalizes longitude.
        if longitude == 180:
            longitude = -180
        code = ""

        # TODO: Populate an array instead of a collection of string ops.
        # chars = []

        # Compute the code.
        # This approach converts each value to an integer after multiplying it by
        # the final precision. This allows us to use only integer operations, so
        # avoiding any accumulation of floating point representation errors.

        # Multiply values by their precision and convert to positive.
        # Force to integers so the division operations will have integer results.
        # Note: Python requires rounding before truncating to ensure precision!
        latVal = int(round((latitude + self.MAX_LAT) * self.FINAL_LAT_PRECISION, 6))
        lngVal = int(round((longitude + self.MAX_LON) * self.FINAL_LON_PRECISION, 6))

        # Compute the grid part of the code if necessary.
        if self.code_length > self.PAIR_CODE_LENGTH:
            for _ in range(self.MAX_CODE_LENGTH - self.PAIR_CODE_LENGTH):
                latDigit = latVal % self.GRID_ROWS
                lngDigit = lngVal % self.GRID_COLUMNS
                ndx = latDigit * self.GRID_COLUMNS + lngDigit
                char = self.ALPHABET[ndx]
                code = char + code
                # Appending to char buf in reverse
                # chars.append(char)
                latVal //= self.GRID_ROWS
                lngVal //= self.GRID_COLUMNS
        else:
            latVal //= pow(self.GRID_ROWS, self.GRID_CODE_LENGTH)
            lngVal //= pow(self.GRID_COLUMNS, self.GRID_CODE_LENGTH)

        # Compute the pair section of the code.
        base = self.ENCODING_BASE
        for _ in range(self.PAIR_CODE_LENGTH // 2):
            # chars.append(self.ALPHABET[lngVal % base])
            # chars.append(self.ALPHABET[latVal % base])
            code = self.ALPHABET[lngVal % base] + code
            code = self.ALPHABET[latVal % base] + code
            latVal //= self.ENCODING_BASE
            lngVal //= self.ENCODING_BASE

        # Add the separator character.
        sep, pos = self.SEP, self.SEP_POSITION
        code = code[:pos] + sep + code[pos:]

        # If we don't need to pad the code, return the requested section.
        if self.code_length >= pos:
            code = code[: self.code_length + 1]
        else:
            code = code[: self.code_length] + "".zfill(pos - self.code_length) + sep
        return code


def encode(lat: float, lon: float, code_length: int = 10) -> str:
    """Create an Encoder instance that encodes Plus Codes using the
    input code length.
    """
    return Encoder(code_length).encode(lat, lon)
