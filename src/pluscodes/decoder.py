import re

from .base import Base
from .geo import Area, Point


class Decoder(Base):
    """
    Decode Plus Codes into the geo boundary.
    Returns a CodeArea object that includes the coordinates of the bounding
    box - the lower left, center and upper right.
    Args:
      code: The Open Location Code to decode.
    Returns:
      A CodeArea object that provides the latitude and longitude of two of the
      corners of the area, the center, and the length of the original code.
    """

    def decode(self, code: str) -> Area:
        """Decode a valid, full Plus Code.

        No explicit validation
        """
        # if not is_full(code):
        #     raise ValueError(
        #         'Passed Open Location Code is not a valid full code - ' + str(code))

        # Strip out separator character (we've already established the code is
        # valid so the maximum is one), and padding characters. Convert to upper
        # case and constrain to the maximum number of digits.
        code = re.sub("[+0]", "", code)
        code = code.upper()
        code = code[: self.MAX_CODE_LENGTH]

        # Initialise the values for each section. We work them out as integers and
        # convert them to floats at the end.
        normalLat = -self.MAX_LAT * self.PAIR_PRECISION
        normalLng = -self.MAX_LON * self.PAIR_PRECISION
        gridLat = 0
        gridLng = 0
        # How many digits do we have to process?
        digits = min(len(code), self.PAIR_CODE_LENGTH)
        # Define the place value for the most significant pair.
        pv = self.PAIR_FIRST_PLACE_VALUE

        # Decode the paired digits.
        for i in range(0, digits, 2):
            normalLat += self._char_index(code[i]) * pv
            normalLng += self._char_index(code[i + 1]) * pv
            if i < digits - 2:
                pv //= self.ENCODING_BASE

        # Convert the place value to a float in degrees.
        fnl_lat_prec = self.FINAL_LAT_PRECISION
        fnl_lon_prec = self.FINAL_LON_PRECISION
        latPrecision = float(pv) / self.PAIR_PRECISION
        lngPrecision = float(pv) / self.PAIR_PRECISION
        # Process any extra precision digits.
        if len(code) > self.PAIR_CODE_LENGTH:
            # Initialise the place values for the grid.
            rowpv = self.GRID_LAT_FIRST_PLACE_VALUE
            colpv = self.GRID_LON_FIRST_PLACE_VALUE
            # How many digits do we have to process?
            digits = min(len(code), self.MAX_CODE_LENGTH)
            for i in range(self.PAIR_CODE_LENGTH, digits):
                digitVal = self._char_index(code[i])
                row = digitVal // self.GRID_COLUMNS
                col = digitVal % self.GRID_COLUMNS
                gridLat += row * rowpv
                gridLng += col * colpv
                if i < digits - 1:
                    rowpv //= self.GRID_ROWS
                    colpv //= self.GRID_COLUMNS

            # Adjust the precisions from the integer values to degrees.
            latPrecision = float(rowpv) / fnl_lat_prec
            lngPrecision = float(colpv) / fnl_lon_prec

        # Merge the values from the normal and extra precision parts of the code.
        lat = float(normalLat) / self.PAIR_PRECISION + float(gridLat) / fnl_lat_prec
        lng = float(normalLng) / self.PAIR_PRECISION + float(gridLng) / fnl_lon_prec

        # Multiple values by 1e14, round and then divide. This reduces errors due
        # to floating point precision.

        sw = Point(lat=round(lat, 14), lon=round(lng, 14))
        ne = Point(lat=round(lat + latPrecision, 14), lon=round(lng + lngPrecision, 14))
        area = Area(sw=sw, ne=ne, code_length=len(code))
        return area
