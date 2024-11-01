import pygame, os

class Track(pygame.sprite.Sprite):
    def __init__(self, dim, trackNum):
        super().__init__()
        self.img = pygame.transform.scale(pygame.image.load(f"./Assets/Backgrounds/track{trackNum}.png"), (dim[0], dim[1])).convert()
        surface = pygame.surface.Surface((dim[0], dim[1])).convert_alpha()
        mask = pygame.transform.scale(pygame.image.load(f"./Assets/TrackMasks/track{trackNum}.png"), (dim[0], dim[1])).convert_alpha()
        surface.blit(mask, (0, 0))
        surface.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(surface)
        self.dim = dim
        self.rect = pygame.Rect(0, 0, dim[0], dim[1])
        
        numFiles = len(os.listdir(f"./Assets/Checkpoints/track{trackNum}"))
        self.checkpoints = []

        for i in range(numFiles):
            surface = pygame.surface.Surface((dim[0], dim[1])).convert_alpha()
            mask = pygame.transform.scale(pygame.image.load(f"./Assets/Checkpoints/track{trackNum}/{i}.png"), (dim[0], dim[1])).convert_alpha()
            surface.blit(mask, (0, 0))
            surface.set_colorkey((0, 0, 0))
            self.checkpoints.append(pygame.mask.from_surface(surface))
