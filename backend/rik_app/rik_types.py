from enum import Enum


# Estonian Tax Identification Number Specification:
# Natural Person TIN lengths: 11 (full), 10 (partial)
# Judicial Person TIN lengths: 8 (full), 7 (partial)
# -------------------------------------------------------------------------------- #
class TINLength(Enum):
    FULL_NATURAL = 11
    FULL_JUDICIAL = 8
    PARTIAL_NATURAL = 10
    PARTIAL_JUDICIAL = 7


# -------------------------------------------------------------------------------- #
class PersonType(Enum):
    NATURAL = "NATURAL"
    JUDICIAL = "JUDICIAL"


# -------------------------------------------------------------------------------- #
__all__ = [
    "TINLength",
    "PersonType",
]
