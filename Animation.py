import pygame

class Animator:
    def __init__(self, dimensions, imgs, fps = 60, maxCycles = -1):
        self.imgs = imgs
        self.current = 0
        self.time = 0
        self.tickRate = 1/fps
        self.dim = dimensions
        self.cycles = 0
        self.maxCycles = maxCycles
        self.slidePos = 0

    def animate(self, WIN, dt):
        if self.cycles > self.maxCycles and self.maxCycles != -1:
            return
        
        self.time += dt
        if self.time >= self.tickRate:
            self.time = 0
            self.current += 1

            if self.current >= len(self.imgs):
                self.current = 0
                self.cycles += 1

        WIN.blit(self.imgs[self.current], (0, 0))
        
    def slide(self, WIN, dt, animTime = 1, reverse = False):
        if abs(self.slidePos) >= self.dim[0]:
            return True
        multiplier = 1

        if reverse:
            multiplier = -1
        self.slidePos -= multiplier * dt * self.dim[0]/animTime

        WIN.blit(self.imgs, (self.slidePos, 0))
        WIN.blit(self.imgs, (self.slidePos + self.dim[0] * multiplier, 0))

        return False
