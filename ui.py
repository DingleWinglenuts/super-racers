import pygame
pygame.init()

# This file contains useful objects relating to the user interface

pressSound = pygame.mixer.Sound("./Assets/Sounds/buttonPress.wav") # Loading sound for when a button is pressed

class Button(): # As the name implies, this is a button object. Rendering and pressing are separate events for more seamless visuals for users
    def __init__(self, txt, fontSize, posX, posY, sizeX = 0, sizeY = 0, bg = True, textDim = False, centre = False):
        self.font = pygame.font.Font("./Assets/Fonts/pixeboy.ttf", int(fontSize))
        self.msg = txt
        self.txt = self.font.render(txt, True, (220, 220, 220))
        self.renderBg = bg
        if textDim:
            sizeX = self.txt.get_width()
            sizeY = self.txt.get_height()
        if centre:
            posX -= self.txt.get_width()//2
            
        if bg:
            self.txt = self.font.render(self.msg, True, (0, 0, 0))
            self.textPos = (posX + sizeX//2 - self.txt.get_width()//2, posY + sizeY//2 - self.txt.get_height()//2) # Centers the text in the middle of the button
            self.rect = pygame.Rect(posX, posY, sizeX, sizeY)
        else:
            self.textPos = (posX, posY)
            self.rect = pygame.Rect(posX, posY, self.txt.get_width(), self.txt.get_height())

    def render(self, WIN): # Displays the button when called and shades it grey when hovered over
        mousePos = pygame.mouse.get_pos()
        colour = (220, 220, 220)
        if self.rect.collidepoint(mousePos):
            colour = (150, 150, 150)

        if not self.renderBg:
            self.txt = self.font.render(self.msg, True, colour)
        if self.renderBg:
            pygame.draw.rect(WIN, colour, self.rect)
        WIN.blit(self.txt, self.textPos)

    def pressed(self, arg = pygame.event.get()): # Checks if the button has been pressed and returns true if so
        mousePos = pygame.mouse.get_pos() 
        if self.rect.collidepoint(mousePos):
            for i in arg:
                if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
                    pressSound.play()
                    return True
                elif i.type == pygame.KEYDOWN and (i.key == pygame.K_SPACE or i.key == pygame.K_RETURN):
                    pressSound.play()
                    return True
        return False
        
class TextBox(): # Again as implied by the name, creates a text box for user text entry (used for saving scores)
    def __init__(self, bound = int, rect = pygame.Rect or tuple, dimensions = tuple, WIN = None, font = pygame.font.Font()):
        self.txt = ""
        self.bound = bound
        self.rect = rect
        self.display_info = dimensions
        self.WIN = WIN
        self.font = font

    def enter(self, eventQueue = None): # Returns true if the enter key has been pressed
        if eventQueue == None:
            queue = pygame.event.get()
        else:
            queue = eventQueue

        for i in queue:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_BACKSPACE:
                    self.txt = self.txt[:-1]
                elif i.key != pygame.K_DELETE and i.key != pygame.K_RETURN and i.key != pygame.K_TAB and i.key != pygame.K_ESCAPE and len(self.txt) < self.bound:
                    self.txt += i.unicode
                elif i.key == pygame.K_RETURN:
                    return True
        return False

    def blit(self): # Displays the text box and any text within
        pygame.draw.rect(self.WIN, (255, 255, 255), self.rect)
        pygame.draw.rect(self.WIN, (0, 0, 0), self.rect, int(self.display_info[1]//1080) + 1)
        txt = self.font.render(self.txt, True, (0, 0, 0))
        self.WIN.blit(txt, (self.rect.x + 5 * self.display_info[0]/1920, self.rect.y + txt.get_height()//4))
