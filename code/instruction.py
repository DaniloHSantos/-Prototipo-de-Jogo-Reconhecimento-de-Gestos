from settings import *

class Instruction(pygame.sprite.Sprite):
    def __init__(self,type,surf,pos,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.type = type
