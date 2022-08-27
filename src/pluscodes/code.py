import re
from typing import Callable

from .decoder import decode
from .encoder import encode
from .geo import Area, Point

# from .validator import Validator


class PlusCode:
    """A data structure containing a full length Plus code.

    Example:
        code = PlusCode(0, 0)

    Attributes:
        code: The default full length (10 character) plus code.
        length: The number of used
        area: The roughly 13m x 13m geographic bounds corresponding to the
            Plus Code.

    """

    # validator = Validator()
    # is_valid: Callable = validator.is_valid
    # is_full: Callable = validator.is_full
    # is_short: Callable = validator.is_short

    def __init__(
        self,
        val: float | int | tuple | Point | str | None = None,
        val2: float | int | None = None,
        *,
        lat: float | int | None = None,
        lon: float | int | None = None,
        code: str | None = None,
        area: Area | None = None,
        code_length: int = 10,
    ):

        # Replace the default encoder with another if a customized code

        if isinstance(val, (float, int)) and isinstance(val2, (float, int)):
            self.code = self.encode(float(val), float(val2))
        elif isinstance(val, str):
            self.code = val.upper()
        elif isinstance(val, tuple):
            # Encode the provided lat / lon to obtain a code.
            self.code = encode(*val, code_length=code_length)
        elif isinstance(val, Point):
            self.code = encode(val.lat, val.lon, code_length)
        elif val is None and lat is not None and lon is not None:
            # When  only kw args are provided,
            self.code = code or encode(float(lat), float(lon), code_length)
        else:
            raise ValueError(f"Unexpected input {val=}")

        self.area = area or decode(self.code)
        self.length: int = len(re.sub("[+0]", "", self.code))

    # @classmethod
    # def is_valid(cls, code: str) -> bool:
    #     """Call cls.validator.is_valid"""
    #     return cls.validator.is_valid(code)

    # @classmethod
    # def is_short(cls, code: str) -> bool:
    #     """Call cls.validator.is_short"""
    #     return cls.validator.is_short(code)

    # @classmethod
    # def is_full(cls, code: str) -> bool:
    #     """Call cls.validator.is_short"""
    #     return cls.validator.is_full(code)
