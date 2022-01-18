

class Bot:
    """A unit capable of changing coordinates
    depending on a given target."""

    def __init__(self, number: int, x: int, y: int):
        self.number = number
        self._x: int = x
        self._y: int = y
        self._target_x = None
        self._target_y = None

    def get_target_x(self) -> int:
        """Gets target of 'x' coordinate of the bot."""
        return self._target_x

    def set_target_x(self, new_target_x: int) -> None:
        """Set target of 'x' coordinate of the bot."""
        self._target_x = new_target_x

    target_x = property(get_target_x, set_target_x)

    def get_target_y(self) -> int:
        """Gets target of 'y' coordinate of the bot."""
        return self._target_y

    def set_target_y(self, new_target_y: int) -> None:
        """Set target of 'y' coordinate of the bot."""
        self._target_y = new_target_y

    target_y = property(get_target_y, set_target_y)

    @property
    def is_moving(self) -> str:
        """Compares coordinates and target,
        returns 'stopped' if then equals
        and 'is moving' if its not."""
        if self._target_x == self._x and \
                self._target_y == self._y:
            return 'stopped'
        else:
            return 'is moving'

