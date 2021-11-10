from __future__ import annotations
import math
from typing import Union


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
        """Returns the dot product of this vector with the 'other' vector."""

        if not isinstance(other, type(self)):
            raise TypeError(f"unsupported operand type(s) for dot product: 'Vector' and '{type(other).__name__}'")

        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector) -> Vector:
        """Returns the cross product of this vector with the 'other' vector."""

        if not isinstance(other, type(self)):
            raise TypeError(f"unsupported operand type(s) for cross product: 'Vector' and '{type(other).__name__}'")

        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def angle_between(self, other: Vector) -> float:
        """Returns the angle in radians between this vector and the 'other' vector."""
        if not isinstance(other, type(self)):
            raise TypeError(
                f"cannot calculate the angle between an object from type 'Vector' and '{type(other).__name__}'"
            )

        return math.acos(self.dot(other) / self.length / other.length)

    def collinear(self, other: Vector) -> bool:
        """Returns wheter or not this vector is collinear with the 'other' vector."""
        if not isinstance(other, type(self)):
            raise TypeError(f"'Vector' object cannot be collinear with object from type '{type(other).__name__}'")
        return self.cross(other) == Vector(0, 0, 0)

    def orthogonal(self, other: Vector) -> bool:
        """Returns wheter or not this vector is orthogonal with the 'other' vector."""
        if not isinstance(other, type(self)):
            raise TypeError(f"'Vector' object cannot be orthogonal with object from type '{type(other).__name__}'")
        return self.dot(other) == 0

    def scalar_triple_product(self, v1: Vector, v2: Vector) -> Union[int, float]:
        """Returns the scalar triple product of this vector with the vectors 'v1' and 'v2'."""
        if not isinstance(v1, type(self)):
            raise TypeError(
                f"unsupported operand type(s) for scalar triple product: 'Vector' and '{type(v1).__name__}'"
            )
        if not isinstance(v2, type(self)):
            raise TypeError(
                f"unsupported operand type(s) for scalar triple product: 'Vector' and '{type(v2).__name__}'"
            )

        return (
            self.x * v1.y * v2.z
            + self.y * v1.z * v2.x
            + self.z * v1.x * v2.y
            - self.x * v1.z * v2.y
            - self.y * v1.x * v2.z
            - self.z * v1.y * v2.x
        )

    def coplanar(self, v1: Vector, v2: Vector) -> bool:
        """Returns wheter or not this vector is coplanar with the vectors 'v1' and 'v2'."""
        if not isinstance(v1, type(self)):
            raise TypeError(f"'Vector' object cannot be coplanar with object from type '{type(v1).__name__}'")
        if not isinstance(v2, type(self)):
            raise TypeError(f"'Vector' object cannot be coplanar with object from type '{type(v2).__name__}'")

        return self.scalar_triple_product(v1, v2) == 0

    def det(self, other: Vector) -> Union[int, float]:
        """Returns the determinant of this vector with the 'other' vector (! vectors must only have two dimensions)"""
        if not isinstance(other, type(self)):
            raise TypeError(
                f"unsupported operand type(s) for calculating determinant: 'Vector' and '{type(other).__name__}'"
            )

        if self.z != 0 or other.z != 0:
            raise ValueError("'Vectors' objects must be two dimensional to calculate the determinant.")

        return self.x * other.y - self.y * other.x

    def __add__(self, other: Vector) -> Vector:
        """Returns the result of the addition of this vector with the 'other' vector."""
        if not isinstance(other, type(self)):
            raise TypeError(f"unsupported operand type(s) for +: 'Vector' and '{type(other).__name__}'")

        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector) -> Vector:
        """Returns the result of the substraction of this vector with the 'other' vector."""
        if not isinstance(other, type(self)):
            raise TypeError(f"unsupported operand type(s) for -: 'Vector' and '{type(other).__name__}'")

        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Union[int, float]) -> Vector:
        """Returns the result of the scalar multiplication of this vector with a number 'other'."""
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other, self.z * other)

        raise TypeError(f"unsupported operand type(s) for *: 'Vector' and '{type(other).__name__}'")

    def __truediv__(self, other: Union[int, float]) -> Vector:
        """Returns the result of the division (scalar multiplication by the inverse) of this vector with a number 'other'."""
        if other == 0:
            raise ZeroDivisionError("Can't divide the vector by 0.")

        if isinstance(other, (int, float)):
            return self.__mul__(1 / other)

        raise TypeError(f"unsupported operand type(s) for /: 'Vector' and '{type(other).__name__}'")

    def __rmul__(self, other: Union[int, float]) -> Vector:
        """Returns the result of the scalar multiplication of this vector with a number 'other'."""
        return self.__mul__(other)

    def __rtruediv__(self, other: Union[int, float]) -> Vector:
        """Returns the result of the division (scalar multiplication by the inverse) of this vector with a number 'other'."""
        return self.__truediv__(other)

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
        """True if the vector is not equal to the null vector."""
        return self.x != 0 and self.y != 0 and self.z != 0

    def __getitem__(self, key):
        if key not in (0, 1, 2):
            raise IndexError(f"Invalid index : {key}.")

        return self.x if key == 0 else self.y if key == 1 else self.z

    def __setitem__(self, key, value):
        if key not in (0, 1, 2):
            raise IndexError(f"Invalid index : {key}.")
        if not isinstance(value, (int, float)):
            raise ValueError(f"'Vector' object cannot contain object from type {type(value).__name__}.")

        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value

    def __setattr__(self, attribute, value):

        attributes = ("x", "y", "z")
        if attribute in attributes:
            if not isinstance(value, (int, float)):
                raise ValueError(f"'Vector' object cannot contain object from type {type(value).__name__}.")
            self.__dict__[attribute] = float(value)
        else:
            self.__dict__[attribute] = value

    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"


if __name__ == "__main__":
    v1 = Vector(-1, -2, 1)
    v2 = Vector(2, 3, 3)
    v3 = Vector(2, 2, 2)

    print(v1.cross(v2))
