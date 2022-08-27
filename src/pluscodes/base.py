class Base:
    """Base class for the Encoder, Decoder, and Validator subclasses defining
    class constants.
    """

    # A separator used to break the code into two parts to aid memorability.
    SEP = "+"

    # The number of characters to place before the separator.
    SEP_POSITION = 8

    # The character used to pad codes.
    PADDING_CHAR = "0"

    # The character set used to encode the values.
    ALPHABET = "23456789CFGHJMPQRVWX"
    VALID_CHARS = set(ch for ch in ALPHABET) | {SEP, PADDING_CHAR}
    ALPHABET_INDEX = {c: i for i, c in enumerate(ALPHABET)}

    # The base to use to convert numbers to/from.
    ENCODING_BASE = len(ALPHABET)

    # The maximum value for latitude in degrees.
    MAX_LAT = 90

    # The maximum value for longitude in degrees.
    MAX_LON = 180

    # The max number of digits to process in a plus code.
    MAX_CODE_LENGTH = 15

    # Default code length using lat/lng pair encoding. The area of such a
    # code is approximately 13x13 meters (at the equator), and should be suitable
    # for identifying buildings. This excludes prefix and separator characters.
    PAIR_CODE_LENGTH = 10

    # First place value of the pairs (if the last pair value is 1).
    PAIR_FIRST_PLACE_VALUE = ENCODING_BASE ** (PAIR_CODE_LENGTH / 2 - 1)

    # Inverse of the precision of the pair section of the code.
    PAIR_PRECISION = ENCODING_BASE**3

    # The resolution values in degrees for each position in the lat/lng pair
    # encoding. These give the place value of each position, and therefore the
    # dimensions of the resulting area.
    PAIR_RESOLUTIONS = [20.0, 1.0, 0.05, 0.0025, 0.000125]

    # Number of digits in the grid precision part of the code.
    GRID_CODE_LENGTH = MAX_CODE_LENGTH - PAIR_CODE_LENGTH

    # Number of columns in the grid refinement method.
    GRID_COLUMNS = 4

    # Number of rows in the grid refinement method.
    GRID_ROWS = 5

    # First place value of the latitude grid (if the last place is 1).
    GRID_LAT_FIRST_PLACE_VALUE = GRID_ROWS ** (GRID_CODE_LENGTH - 1)

    # First place value of the longitude grid (if the last place is 1).
    GRID_LON_FIRST_PLACE_VALUE = GRID_COLUMNS ** (GRID_CODE_LENGTH - 1)

    # Multiply latitude by this much to make it a multiple of the finest
    # precision.
    FINAL_LAT_PRECISION = PAIR_PRECISION * GRID_ROWS ** (
        MAX_CODE_LENGTH - PAIR_CODE_LENGTH
    )

    # Multiply longitude by this much to make it a multiple of the finest
    # precision.
    FINAL_LON_PRECISION = PAIR_PRECISION * GRID_COLUMNS ** (
        MAX_CODE_LENGTH - PAIR_CODE_LENGTH
    )

    # Minimum length of a code that can be shortened.
    MIN_TRIMMABLE_CODE_LEN = 6

    # Degree length of length 10 Plus Codes.
    GRID_SIZE_DEGREES = 0.000125

    def _char_index(self, char: str) -> int:
        """Find the index in the code alphabet for the input character."""
        return self.ALPHABET_INDEX[char]
