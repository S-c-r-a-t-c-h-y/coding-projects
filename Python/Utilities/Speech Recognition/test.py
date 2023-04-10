import enum


@enum.unique
class Engines(enum.Enum):
    GOOGLE = enum.auto()
    GOOGLE_CLOUD = enum.auto()
    BING = enum.auto()
    HOUNDIFY = enum.auto()
    IBM = enum.auto()
    SPHINX = enum.auto()
    WIT = enum.auto()


a = Engines.GOOGLE
b = 2

print(b in Engines)
