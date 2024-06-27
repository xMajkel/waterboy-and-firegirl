from game.crystal import BLUE, RED, Crystal
from game.door import LavaDoor, WaterDoor
from game.level import LevelBase
from game.platform import (AcidPlatform, LavaPlatform, MovingPlatform,
                           Platform, WaterPlatform)


class Level2(LevelBase):
    def __init__(self, game):
        super().__init__(game, (125, 550), (625, 550))
        self.platforms = [
            Platform(0, 580, 800, 20),
            Platform(0, 0, 800, 20),
            Platform(0, 0, 20, 600),
            Platform(780, 0, 20, 600),

            Platform(100, 500, 600, 20),

            Platform(50, 425, 150, 20),
            Platform(600, 425, 150, 20),

            Platform(200, 300, 400, 20),

            MovingPlatform(150, 225, 100, 20, True, False, 400, 0, 3),

            WaterPlatform(410, 580-1, 80, 10),
            WaterPlatform(615, 425-1, 120, 10),
            LavaPlatform(300, 580-1, 80, 10),
            LavaPlatform(65, 425-1, 120, 10),
            AcidPlatform(300, 500-1, 200, 10),
            AcidPlatform(350, 300-1, 100, 10),

            Platform(50, 150, 200, 20),
            Platform(550, 150, 200, 20),

            Platform(20, 330, 100, 20),
            Platform(800-20-100, 330, 100, 20),
           
            Platform(400-10, 450, 20, 60),

        ]
        self.crystals = [
            Crystal(125, 360, (255, 0, 0), RED),
            Crystal(645, 360, (0, 0, 255), BLUE),
            
            Crystal(250, 270, (255, 0, 0), RED),
            Crystal(550, 270, (0, 0, 255), BLUE),
            
            Crystal(150, 120, (255, 0, 0), RED),
            Crystal(650, 120, (0, 0, 255), BLUE),
        ]
        self.waterDoor = WaterDoor(50, 50, 50, 100, game.textures["DOORS"]["BLUE"])
        self.lavaDoor = LavaDoor(700, 50, 50, 100, game.textures["DOORS"]["RED"])
