import math
from typing import Union
from __future__ import annotations


class Vector:
    """Class that represents a vector"""

    def __init__(self, x, y=0, z=0) -> None:
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    @property
    def length(self) -> float:
        """Length of the vector in 3D space."""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self) -> Vector:
        """Returns a vector with length 1 and the same direction as the current vector."""
        return self.__mul__(1 / self.length)

    def dot(self, other: Vector) -> Union[int, float]:
        """Returns the dot product of this vector with the other vector."""

        if not isinstance(other, type(self)):
            raise TypeError(f"unsupported operand type(s) for dot product: 'Vector' and '{type(other).__name__}'")

        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector) -> Vector:
        """Returns the cross product of this vector with the other vector."""

        if not isinstance(other, type(self)):
            raise TypeError(f"unsupported operand type(s) for cross product: 'Vector' and '{type(other).__name__}'")

        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - other.y * self.x,
        )

    def __add__(self, other: Vector) -> Vector:
        if not isinstance(other, type(self)):
            raise TypeError(f"unsupported operand type(s) for +: 'Vector' and '{type(other).__name__}'")

        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector) -> Vector:
        if not isinstance(other, type(self)):
            raise TypeError(f"unsupported operand type(s) for -: 'Vector' and '{type(other).__name__}'")

        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Union[int, float]) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other, self.z * other)

        raise TypeError(f"unsupported operand type(s) for *: 'Vector' and '{type(other).__name__}'")

    def __truediv__(self, other: Union[int, float]) -> Vector:

        if other == 0:
            raise ZeroDivisionError("Can't divide the vector by 0.")

        if isinstance(other, (int, float)):
            return self.__mul__(1 / other)

        raise TypeError(f"unsupported operand type(s) for /: 'Vector' and '{type(other).__name__}'")

    def __neg__(self) -> Vector:
        return self.__mul__(-1)

    def __eq__(self, other: Vector) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __neq__(self, other: Vector) -> bool:
        if not isinstance(other, type(self)):
            return True
        return self.x != other.x or self.y != other.y or self.z != other.z

    def __bool__(self) -> bool:
        return self.x != 0 and self.y != 0 and self.z != 0

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y}, {self.z})"


v1 = Vector(3, -3, 1)
v2 = Vector(-12, 12, -4)

v4 = v1.cross(v2)
print(v4)
