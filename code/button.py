from settings import *

class Button:
    def __init__(self,image,pos,surface):
        self.image = image
        self.rect = self.image.get_frect(center=pos)
        self.pos = pos
        self.surface = surface

    def draw(self):
        self.surface.blit(self.image,self.rect)

    def check_click(self,click):
        if self.rect.collidepoint(click):
            return True