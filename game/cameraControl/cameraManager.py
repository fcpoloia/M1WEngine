import pygame


class CameraManager(pygame.sprite.Group):

    """Camera Manager
    This class will render each sprite in the game at an offset relative to the players
    x and y. As the positions are manipulated, there will be an illusion of camera
    movement.

    Attributes
    ----------
    playerCharacter : Player
        the currently shown frame represented by an index
    displaySurface : Surface
        the game surface in which to render all sprites
    offset : vector2
        the offset at which to render all sprites
    halWidth : int
        half the display surface width
    halfHeight : int
        half the display surface height

    Methods
    -------
    camera_draw()
        Renders all sprites relative to the player character position
    """

    # initialize all groups and their current positions
    def __init__(self, playerCharacter):
        """Constructor
        This method will instantiate the camera controller.
        A single camera controller should be used to manage all rendered sprites.
        Parameters
        ----------
        playerCharacter: the player character
        """

        super().__init__()
        surfaceX = 0
        surfaceY = 1
        self.displaySurface = pygame.display.get_surface()
        self.halfWidth = (
            self.displaySurface.get_size()[surfaceX] // 2
        )  # floor division, returns int
        self.halfHeight = (
            self.displaySurface.get_size()[surfaceY] // 2
        )  # floor division, returns int

        self.offset = pygame.math.Vector2()
        self.playerCharacter = playerCharacter

    def camera_update(self):
        """camera_update
        This method will set the direction of camera sprites to be the
        opposite direction of the player's heading.
        """

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            # offset = sprite.rect.topleft - self.offset
            prevDirection = sprite.compass
            sprite.compass = self.playerCharacter.compass * -1
            sprite.move(self.playerCharacter.speed)
            sprite.compass = prevDirection