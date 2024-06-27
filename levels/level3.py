from game.crystal import BLUE, RED, Crystal
from game.door import LavaDoor, WaterDoor
from game.level import LevelBase
from game.platform import (AcidPlatform, LavaPlatform, MovingPlatform,
                           Platform, WaterPlatform)


class Level3(LevelBase):
    def __init__(self, game):
        super().__init__(game, (75,90), (690,90))
        self.platforms = [
            Platform(0, 580, 800, 20),
            Platform(0, 0, 800, 20),
            Platform(0, 0, 20, 600),
            Platform(800-20, 0, 20, 600),

            Platform(20, 150+20, 350-20, 20),
            Platform(450, 150+20, 350, 20),

            WaterPlatform(450, 150-1+20, 50, 10),
            LavaPlatform(300, 150-1+20, 50, 10),
            MovingPlatform(150,250+20,100,20,True,False,400,0,1),

            Platform(100, 250+20, 20, 250),
            Platform(700-20, 250+20, 20, 250),

            AcidPlatform(120, 300+20, 600-40, 40),
            Platform(120, 340+20, 600-40, 20),

            Platform(225, 500, 350, 150),
            Platform(400-10, 370, 20, 130),

            
            
        ]
        self.crystals = [
            Crystal(150, 225, (255, 0, 0), RED),
            Crystal(600, 225, (0, 0, 255), BLUE),
           
            Crystal(620, 525, (255, 0, 0), RED),
            Crystal(165, 525, (0, 0, 255), BLUE),
        ]
        self.waterDoor = WaterDoor(310, 400, 50, 100,game.textures["DOORS"]["BLUE"])
        self.lavaDoor = LavaDoor(440, 400, 50, 100,game.textures["DOORS"]["RED"])