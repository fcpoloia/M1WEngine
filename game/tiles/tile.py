"""This module contains the Tile class."""
import pygame
from direction import Direction


class Tile(pygame.sprite.Sprite):
    """Base class for all game :func:`Sprite<pygame.sprite.Sprite>`.

    Attributes
    ----------
    direction: pygame.math.Vector2
        the x and y direction of movement. This will be in a range
        of -1 to 1 where 0 means no movement
    movementTracker: dict[str, float]
        Contains how far the entity has traveled without moving
    colorKeyWhite: tuple
        Tuple to hold a white RGB value
    colorKeyBlack: tuple
        Tuple to hold a black RGB value

    Methods
    -------
    move(self, speed: int)
        Handles movement of the entity
    move_left(self, speed: int)
        Moves left
    move_right(self, speed: int)
        Moves right
    move_up(self, speed: int)
        Moves up
    move_down(self, speed: int)
        Moves down
    update_movement_tracker(self)
        Tracks where to move
    set_tile(self, x: int, y: int, surface: pygame.surface)
        sets all info for a background tile
    _move_left(self, speed: int)
        Internal move left
    _move_right(self, speed: int)
        Internal move right
    _move_up(self, speed: int)
        Internal move up
    _move_down(self, speed: int)
        Internal move down
    """

    # other init options: sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))
    def __init__(self, groups: pygame.sprite.Group):
        """Initialize a tile.

        Parameters
        ----------
        groups: pygame.sprite.Group
            The groups this sprite is a part of
        """
        super().__init__(groups)
        self.compass: pygame.math.Vector2 = pygame.math.Vector2()
        self.movementTracker = {"vertical": 0.0, "horizontal": 0.0}

        # r,g,b vals for key color
        self.colorKeyWhite = (255, 255, 255)
        self.colorKeyBlack = (0, 0, 0)

    def setColorKeyBlack(self):
        """Set the sprite alpha channel to ignore black backgrounds."""
        self.image.set_colorkey(self.colorKeyBlack, pygame.RLEACCEL)

    def setColorKeyWhite(self):
        """Set the sprite alpha channel to ignore white backgrounds."""
        self.image.set_colorkey(self.colorKeyWhite, pygame.RLEACCEL)

    def move(self, speed: int):
        """Handle movement of the tile.

        Updates position of the tile using current heading and speed.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        # move each time a tracker is 1 or -1 and then reset the tracker
        self.update_movement_tracker()

        up = Direction.up
        down = Direction.down
        left = Direction.left
        right = Direction.right

        if self.movementTracker["vertical"] <= up:
            self._move_up(speed)
            self.movementTracker["vertical"] += down
        elif self.movementTracker["vertical"] >= down:
            self._move_down(speed)
            self.movementTracker["vertical"] += up

        if self.movementTracker["horizontal"] <= left:
            self._move_left(speed)
            self.movementTracker["horizontal"] += right
        elif self.movementTracker["horizontal"] >= right:
            self._move_right(speed)
            self.movementTracker["horizontal"] += left

    def move_right(self, speed: int):
        """Move to the right.

        Update the compass and move to the right.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        self.compass.x = Direction.right
        self.compass.y = 0
        self._move_right(speed)

    def move_left(self, speed: int):
        """Move to the left.

        Update the compass and move to the left.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        self.compass.x = Direction.right
        self.compass.y = 0
        self._move_left(speed)

    def move_up(self, speed: int):
        """Move up.

        Update the compass and move up.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        self.compass.x = 0
        self.compass.y = Direction.up
        self._move_up(speed)

    def move_down(self, speed: int):
        """Move down.

        Update the compass and move down.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        self.compass.x = 0
        self.compass.y = Direction.down
        self._move_down(speed)

    def update_movement_tracker(self):
        """Update movement tracker.

        Keeps tracker of how far the entity has moved without yet accounting for that
        movement. Each time a movement of 1 pixel is detected, the move will be made,
        and the tracker will be modified by that move distance in pixels towards 0.
        Speed can multiply the number of pixels moved at a time.
        """
        self.movementTracker["horizontal"] += self.compass.x
        self.movementTracker["vertical"] += self.compass.y

    def set_tile(self, coords: tuple, surface: pygame.Surface):
        """Set the position and surface of a tile.

        Parameters
        ----------
        coords: tuple
            The x and y coordinate of the tile
        surface: pygame.Surface
            The :func:`Sprite<pygame.sprite.Sprite>` image to display
        """
        self.image = surface
        self.rect = self.image.get_rect(topleft=coords)
        self.hitbox = self.rect

    def die(self):
        """Remove the sprite from all groups."""
        self.kill()

    def _move_left(self, speed: int):
        """Move to the left.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        move_pixels_x = -1 * speed
        move_pixels_y = 0
        self.rect.move_ip(move_pixels_x, move_pixels_y)
        self.hitbox.center = self.rect.center

    def _move_right(self, speed: int):
        """Move to the right.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        move_pixels_x = speed
        move_pixels_y = 0
        self.rect.move_ip(move_pixels_x, move_pixels_y)
        self.hitbox.center = self.rect.center

    def _move_up(self, speed: int):
        """Move up.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        move_pixels_x = 0
        move_pixels_y = -1 * speed
        self.rect.move_ip(move_pixels_x, move_pixels_y)
        self.hitbox.center = self.rect.center

    def _move_down(self, speed: int):
        """Move down.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        move_pixels_x = 0
        move_pixels_y = speed
        self.rect.move_ip(move_pixels_x, move_pixels_y)
        self.hitbox.center = self.rect.center
