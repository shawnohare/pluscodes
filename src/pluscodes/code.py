from typing import Callable, TypeAlias

from .decoder import Decoder
from .encoder import Encoder
from .geo import Area, Point
from .types import Number
from .validator import Validator


class PlusCode:
    """A data structure containing a full length Plus code.

    Example:

    Attributes:
        code: The default full length (10 character) plus code.
        area: The roughly 13m x 13m geographic bounds corresponding to the
            Plus Code.

    """

    encode: Callable = Encoder().encode
    decode: Callable = Decoder().decode
    validator = Validator()

    def __init__(
        self,
        val: Number | tuple | Point | str | None = None,
        val2: Number | None = None,
        *,
        lat: Number | None = None,
        lon: Number | None = None,
        code: str | None = None,
        area: Area | None = None,
    ):

        if isinstance(val, float) or isinstance(val, int):
            self.code = self.encode(val, val2)
        elif isinstance(val, str):
            self.code = val
        elif isinstance(val, tuple):
            # Encode the provided lat / lon to obtain a code.
            self.code = self.encode(*val)
        elif isinstance(val, Point):
            self.code = self.encode(val.lat, val.lon)
        elif val is None:
            # When  only kw args are provided,
            self.code = code or self.encode(lat, lon)
        else:
            raise ValueError(f"Unexpected input {val=}")

        self.area = area or self.decode(self.code)

    @classmethod
    def is_valid(cls, code: str) -> bool:
        """Call cls.validator.is_valid"""
        return cls.validator.is_valid(code)

    @classmethod
    def is_short(cls, code: str) -> bool:
        """Call cls.validator.is_short"""
        return cls.validator.is_short(code)

    @classmethod
    def is_full(cls, code: str) -> bool:
        """Call cls.validator.is_short"""
        return cls.validator.is_full(code)
