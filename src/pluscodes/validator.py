from .base import Base


class Validator(Base):
    def is_valid(self, code: str) -> bool:
        """
        Determines if a Plus code is valid.
        To be valid, all characters must be from the Plus Code character
        set with at most one separator. The separator can be in any even-numbered
        position up to the eighth digit.
        """
        code = code.upper()

        # Is it the only character?
        if len(code) == 1 or code.count(self.SEP) > 1:
            return False

        # The separator is required.
        sep = code.find(self.SEP)

        # Is it in an illegal position?
        if sep == -1 or sep > self.SEP_POSITION or sep % 2 == 1:
            return False

        # We can have an even number of padding characters before the separator,
        # but then it must be the final character.
        pad = code.find(self.PADDING_CHAR)
        if pad != -1:
            # Short codes cannot have padding
            if sep < self.SEP_POSITION:
                return False
            # Not allowed to start with them!
            if pad == 0:
                return False

            # There can only be one group and it must have even length.
            rpad = code.rfind(self.PADDING_CHAR) + 1
            pads = code[pad:rpad]
            if len(pads) % 2 == 1 or pads.count(self.PADDING_CHAR) != len(pads):
                return False
            # If the code is long enough to end with a separator, make sure it does.
            if not code.endswith(self.SEP):
                return False

        # If there are characters after the separator, make sure there isn't just
        # one of them (not legal).
        if len(code) - sep - 1 == 1:
            return False

        # Check the code contains only valid characters.
        for ch in code:
            if ch not in self.VALID_CHARS:
                return False
        return True

    def is_short(self, code: str) -> bool:
        """
        Determines if a code is a valid short code.
        A short Open Location Code is a sequence created by removing four or more
        digits from an Open Location Code. It must include a separator
        character.
        """
        pos = self.SEP_POSITION
        return self.is_valid(code) and (0 < code.find(self.SEP) < pos)

    def is_full(self, code: str) -> bool:
        """
        Determines if a code is a valid full Open Location Code.
        Not all possible combinations of Open Location Code characters decode to
        valid latitude and longitude values. This checks that a code is valid
        and also that the latitude and longitude values are legal. If the prefix
        character is present, it must be the first character. If the separator
        character is present, it must be after four characters.
        """
        if not self.is_valid(code) or self.is_short(code):
            return False

        idx = self.ALPHABET_INDEX

        # Fetch initial values for lat and lon.
        first_lat = idx[code[0]] * self.ENCODING_BASE
        first_lon = idx[code[1]] * self.ENCODING_BASE

        res = True
        if (first_lat >= self.MAX_LAT * 2) or (first_lon >= self.MAX_LON * 2):
            res = False
        return res
