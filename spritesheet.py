import pygame

# This file contains an object that allows developers to make use of spritesheets and split them up according to their needs

class Spritesheet():
    def __init__(self, sheet): # Stores the spritesheet image
        self.sheet = sheet

    def getSprite(self, posX, posY, sizeX, sizeY, scale): # Gets an individual sprite
        img = pygame.Surface((sizeX, sizeY)).convert_alpha()
        img.blit(self.sheet, (0, 0), (posX, posY, sizeX, sizeY))
        img = pygame.transform.scale(img, (sizeX * scale, sizeY * scale))
        img.set_colorkey((0, 0, 0))
        return img
    
    def getSprites(self, spriteWidth, spriteHeight, rows, scale = 1): # Gets all sprites through the use of iteration and the getSprite function (spritesheets must be correctly formatted for this to work.)
        sprites = []

        for j in range(rows):
            sprites.append([])
            for i in range(self.sheet.get_width()//spriteWidth):
                sprites[j].append(self.getSprite(i * spriteWidth, j * spriteHeight, spriteWidth, spriteHeight, scale))
                
        return sprites
