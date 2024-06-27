from game.crystal import BLUE, RED, Crystal
from game.door import LavaDoor, WaterDoor
from game.level import LevelBase
from game.platform import (AcidPlatform, LavaPlatform, MovingPlatform,
                           Platform, WaterPlatform)


class Level1(LevelBase):
    def __init__(self, game):
        super().__init__(game, (100, 600), (100, 500))
        self.platforms = [
            Platform(0, 580, 800, 20),
            Platform(0, 0, 800, 20),
            Platform(0, 0, 20, 600),
            Platform(800-20, 0, 20, 600),
            
            Platform(0, 400, 700-20, 20),

            Platform(0, 500, 150, 20),

            Platform(700-20, 500, 100, 100),

            Platform(20, 200, 350-20, 20),
            Platform(450, 200, 350, 20),
            Platform(150, 300, 100, 100),

            MovingPlatform(350, 200, 100, 20, False, True, 0, 200, 1),

            WaterPlatform(250, 580-1, 80, 10),
            LavaPlatform(400, 580-1, 80, 10),
            AcidPlatform(500, 400-1, 80, 10),
        ]
        self.crystals = [
            Crystal(425,525, (255, 0, 0), RED),
            Crystal(285, 525, (0, 0, 255), BLUE),
            
            Crystal(50,350, (255, 0, 0), RED),
            Crystal(100, 350, (0, 0, 255), BLUE),
            
            Crystal(175,150, (255, 0, 0), RED),
            Crystal(600, 150, (0, 0, 255), BLUE),
        ]
        self.waterDoor = WaterDoor(50, 100, 50, 100,game.textures["DOORS"]["BLUE"])
        self.lavaDoor = LavaDoor(800-100, 100, 50, 100,game.textures["DOORS"]["RED"])
