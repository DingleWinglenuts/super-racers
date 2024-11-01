import pygame, math, json

class Player(pygame.sprite.Sprite):
    def __init__(self, dim, colour):
        super().__init__()
        self.colour = colour
        self.dim = dim
        self.defImg = pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load(f"./Assets/Players/{colour}.png"), 4 * dim[1]/1080), 90).convert_alpha()
        self.currentImg = self.defImg
        surface = pygame.surface.Surface((self.defImg.get_width(), self.defImg.get_height())).convert_alpha()
        surface.fill((0, 0, 0))
        surface.blit(self.defImg, (0, 0))
        surface.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(surface)
        self.laps = 0
        self.rotation = 0
        self.acceleration = 0
        self.rect = self.defImg.get_rect()
        self.posX = 0
        self.posY = 0
        self.maxAccel = -700
        self.minAccel = 180
        self.nextPoint = 0
        self.laps = -1
        self.blitLaps = 0
        self.lapsFont = pygame.font.Font("./Assets/Fonts/pixeboy.ttf", int(dim[1]//6))
        self.win = False

        file = open("./Assets/config.json", "r")
        players = json.load(file)
        file.close()

        if colour == "red":
            self.movementKeys = [players[0]["up"], players[0]["down"]]
            self.turnKeys = [players[0]["left"], players[0]["right"]]
        else:
            self.movementKeys = [players[1]["up"], players[1]["down"]]
            self.turnKeys = [players[1]["left"], players[1]["right"]]

    def move(self, WIN, dt, track):
        keys = pygame.key.get_pressed()

        maxAccel = self.maxAccel
        minAccel = self.minAccel

        if keys[self.turnKeys[0]]:
            self.rotation += 200 * dt/(dt + 1)
            x, y = self.rect.center
            self.currentImg = pygame.transform.rotate(self.defImg, self.rotation)
            surface = pygame.surface.Surface((self.currentImg.get_width(), self.currentImg.get_height())).convert_alpha()
            surface.blit(self.currentImg, (0, 0))
            surface.set_colorkey((0, 0, 0))
            self.mask = pygame.mask.from_surface(surface)
            self.rect = self.currentImg.get_rect()
            self.rect.center = (x, y)
            self.posX = self.rect.x
            self.posY = self.rect.y
            maxAccel *= 1 - 10 * dt
        elif keys[self.turnKeys[1]]:
            self.rotation -= 200 * dt/(dt + 1)
            x, y = self.rect.center
            self.currentImg = pygame.transform.rotate(self.defImg, self.rotation)
            surface = pygame.surface.Surface((self.currentImg.get_width(), self.currentImg.get_height())).convert_alpha()
            surface.blit(self.currentImg, (0, 0))
            surface.set_colorkey((0, 0, 0))
            self.mask = pygame.mask.from_surface(surface)
            self.rect = self.currentImg.get_rect()
            self.rect.center = (x, y)
            self.posX = self.rect.x
            self.posY = self.rect.y
            maxAccel *= 1 - 10 * dt

        playerBits = self.mask.count()
        offset = (track.rect.x - self.posX), (track.rect.y - self.posY)

        if self.mask.overlap(track.checkpoints[self.nextPoint], (-self.rect.x, -self.rect.y)):
            if self.nextPoint == 0:
                self.laps += 1
                if self.laps != 0:
                    self.blitLaps += 1
            self.nextPoint += 1

        if self.nextPoint > len(track.checkpoints) - 1:
            self.nextPoint = 0

        if not playerBits == self.mask.overlap_area(track.mask, offset):
            maxAccel *= 0.2
            minAccel *= 0.2
            self.acceleration *= 1 - dt

        if keys[self.movementKeys[0]] and self.acceleration > maxAccel:
            self.acceleration -= 1000 * dt
        elif keys[self.movementKeys[1]] and self.acceleration < minAccel:
            self.acceleration += 500 * dt
        else:
            self.acceleration *= 1 - 2.5 * dt

        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360

        moveX = self.acceleration * dt * math.sin(math.radians(self.rotation + 90))
        moveY = self.acceleration * dt * math.cos(math.radians(self.rotation + 90))

        self.posX += moveX
        self.posY += moveY

        if self.posX < 0:
            self.posX = 0
        elif self.posX > self.dim[0] - self.rect.w:
            self.posX = self.dim[0] - self.rect.w

        if self.posY < 0:
            self.posY = 0
        elif self.posY > self.dim[1] - self.rect.h:
            self.posY = self.dim[1] - self.rect.h

        self.rect.x = self.posX
        self.rect.y = self.posY

        checkpointOutline = track.checkpoints[self.nextPoint].outline()
        pygame.draw.lines(WIN, self.colour, 0, checkpointOutline)

        self.lapsImg = self.lapsFont.render(str(self.blitLaps), True, (255, 255, 255), self.colour)

        WIN.blit(self.currentImg, self.rect)

        if self.laps >= 10:
            self.win = True
