from enum import Enum


class PieceType(Enum):
    BORDER = 0
    CORNER = 1
    CENTER = 2


class SideType(Enum):
    HEAD = 0
    HOLE = 1
    FLAT = 2

    def opposite(self):
        return {
            SideType.HEAD: SideType.HOLE,
            SideType.HOLE: SideType.HEAD,
            SideType.FLAT: SideType.FLAT,
        }[self]


class SidePosition(Enum):
    RIGHT = 0
    TOP = 1
    LEFT = 2
    BOTTOM = 3

    # Get the opposite side position
    def opposite(self):
        return {
            SidePosition.TOP: SidePosition.BOTTOM,
            SidePosition.RIGHT: SidePosition.LEFT,
            SidePosition.BOTTOM: SidePosition.TOP,
            SidePosition.LEFT: SidePosition.RIGHT,
        }[self]

    def turn_clockwise(self):
        return {
            SidePosition.TOP: SidePosition.RIGHT,
            SidePosition.RIGHT: SidePosition.BOTTOM,
            SidePosition.BOTTOM: SidePosition.LEFT,
            SidePosition.LEFT: SidePosition.TOP,
        }[self]

    def turn_counter_clockwise(self):
        return {
            SidePosition.TOP: SidePosition.LEFT,
            SidePosition.RIGHT: SidePosition.TOP,
            SidePosition.BOTTOM: SidePosition.RIGHT,
            SidePosition.LEFT: SidePosition.BOTTOM,
        }[self]
