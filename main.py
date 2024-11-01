import pygame, spritesheet, Animation, pyTime, ui, player, random, pyTrack, instructions
pygame.init()

time = pyTime.PyTime()

WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Racers")
icon = pygame.image.load("./Assets/Players/red.png")
pygame.display.set_icon(icon)

menuSheet = spritesheet.Spritesheet(pygame.transform.scale(pygame.image.load(f"./Assets/Backgrounds/mainMenuBg{random.randint(1, 4)}.png"), (WIDTH * 2, HEIGHT)))
menuImgs = menuSheet.getSprites(WIDTH, HEIGHT, 1)[0]
menuBg = Animation.Animator((WIDTH, HEIGHT), menuImgs, 30)

menuFont = pygame.font.Font("./Assets/Fonts/pixeboy.ttf", HEIGHT//4)
menuTxt = menuFont.render("super racers", True, (255, 255, 255))

playButton = ui.Button("Play", HEIGHT//8, WIDTH//24, HEIGHT//3, bg = False)
controlsButton = ui.Button("controls", HEIGHT//8, WIDTH//24, HEIGHT//3 + HEIGHT//8, bg = False)
quitButton = ui.Button("quit", HEIGHT//8, WIDTH//24, HEIGHT//3 + HEIGHT//4, bg = False)

menuRun = True
fullbreak = False
backToMenu = False

while menuRun:
    WIN.fill((0, 0, 0))
    menuBg.animate(WIN, time.deltaTime)
    WIN.blit(menuTxt, (WIDTH//2 - menuTxt.get_width()//2, HEIGHT//10))

    eventQueue = pygame.event.get()

    playButton.render(WIN)
    controlsButton.render(WIN)
    quitButton.render(WIN)

    pygame.display.update()#

    backToMenu = False

    if controlsButton.pressed(eventQueue):
        controlsRun = True
        controlsBG = pygame.transform.scale(pygame.image.load("./Assets/Backgrounds/controlsMenu.png"), (WIDTH, HEIGHT)).convert()
        animation = Animation.Animator((WIDTH, HEIGHT), controlsBG)
        
        controlsFont = pygame.font.Font("./Assets/Fonts/pixeboy.ttf", HEIGHT//6)
        header = controlsFont.render("controls", True, (255, 255, 255))

        reverse = True
        controls = True
        slideButton = ui.Button(">", HEIGHT//6, WIDTH//2 + 5 * WIDTH//12, HEIGHT//2 - HEIGHT//12, bg = False)
        move = False
        keyReg = False
        replaceKey = None
        p = 0

        keyRegTxt = controlsFont.render("press new key", True, (255, 255, 255))

        currentControls = instructions.Controls()

        keysFont = pygame.font.Font("./Assets/Fonts/pixeboy.ttf", HEIGHT//10)

        accelerate = keysFont.render("accelerate:", True, (255, 255, 255))
        decelerate = keysFont.render("decelerate:", True, (255, 255, 255))
        left = keysFont.render("left:", True, (255, 255, 255))
        right = keysFont.render("right:", True, (255, 255, 255))

        p1Buttons = {
            "up":ui.Button(currentControls.data[0]["unicode"]["up"], HEIGHT//10, WIDTH//3, HEIGHT//3, textDim = True, centre = True)
        }
        p1Buttons["down"] = ui.Button(currentControls.data[0]["unicode"]["down"], HEIGHT//10, WIDTH//3, HEIGHT//3 + HEIGHT//128 + HEIGHT//10, textDim = True, centre = True)
        p1Buttons["left"] = ui.Button(currentControls.data[0]["unicode"]["left"], HEIGHT//10, WIDTH//3, HEIGHT//3 + 2 * HEIGHT//128 + 2 * HEIGHT//10, textDim = True, centre = True)
        p1Buttons["right"] = ui.Button(currentControls.data[0]["unicode"]["right"], HEIGHT//10, WIDTH//3, HEIGHT//3 + 3 * HEIGHT//128 + 3 * HEIGHT//10, textDim = True, centre = True)

        p2Buttons = {
            "up":ui.Button(currentControls.data[1]["unicode"]["up"], HEIGHT//10, 2 * WIDTH//3, HEIGHT//3, textDim = True, centre = True)
        }
        p2Buttons["down"] = ui.Button(currentControls.data[1]["unicode"]["down"], HEIGHT//10, 2 * WIDTH//3, HEIGHT//3 + HEIGHT//128 + HEIGHT//10, textDim = True, centre = True)
        p2Buttons["left"] = ui.Button(currentControls.data[1]["unicode"]["left"], HEIGHT//10, 2 * WIDTH//3, HEIGHT//3 + 2 * HEIGHT//128 + 2 * HEIGHT//10, textDim = True, centre = True)
        p2Buttons["right"] = ui.Button(currentControls.data[1]["unicode"]["right"], HEIGHT//10, 2 * WIDTH//3, HEIGHT//3 + 3 * HEIGHT//128 + 3 * HEIGHT//10, textDim = True, centre = True)

        resetButton = ui.Button("reset to default", HEIGHT//15, WIDTH//2, HEIGHT - HEIGHT//24, textDim = True, centre = True)

        while controlsRun:
            WIN.fill((0, 0, 0))
            WIN.blit(controlsBG, (0, 0))

            eventQueue = pygame.event.get()

            if not move:
                WIN.blit(header, (WIDTH//2 - header.get_width()//2, HEIGHT//64))
                slideButton.render(WIN)

                if controls:
                    WIN.blit(accelerate, (WIDTH//20, HEIGHT//3))
                    WIN.blit(decelerate, (WIDTH//20, HEIGHT//3 + HEIGHT//128 + HEIGHT//10))
                    WIN.blit(left, (WIDTH//20, HEIGHT//3 + 2 * HEIGHT//128 + 2 * HEIGHT//10))
                    WIN.blit(right, (WIDTH//20, HEIGHT//3 + 3 * HEIGHT//128 + 3 * HEIGHT//10))

                    for i in p1Buttons:
                        p1Buttons[i].render(WIN)

                    for i in p2Buttons:
                        p2Buttons[i].render(WIN)

                    if keyReg:
                        WIN.blit(keyRegTxt, (WIDTH//2 - keyRegTxt.get_width()//2, HEIGHT//2 - keyRegTxt.get_height() - HEIGHT//64))

                    resetButton.render(WIN)
                    
            else:
                move = not animation.slide(WIN, time.deltaTime, 0.8, reverse)

            pygame.display.update()

            for i in eventQueue:
                if i.type == pygame.QUIT:
                    fullbreak = True
                    break

                if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                    if keyReg:
                        keyReg = False
                    else:
                        controlsRun = False
                        break
                elif i.type == pygame.KEYDOWN and keyReg:
                    currentControls.changeKey(p, replaceKey, i.key, pygame.key.name(i.key))
                    keyReg = False
                    if p == 0:
                        p1Buttons = {
                            "up":ui.Button(currentControls.data[0]["unicode"]["up"], HEIGHT//10, WIDTH//3, HEIGHT//3, textDim = True, centre = True)
                        }
                        p1Buttons["down"] = ui.Button(currentControls.data[0]["unicode"]["down"], HEIGHT//10, WIDTH//3, HEIGHT//3 + HEIGHT//128 + HEIGHT//10, textDim = True, centre = True)
                        p1Buttons["left"] = ui.Button(currentControls.data[0]["unicode"]["left"], HEIGHT//10, WIDTH//3, HEIGHT//3 + 2 * HEIGHT//128 + 2 * HEIGHT//10, textDim = True, centre = True)
                        p1Buttons["right"] = ui.Button(currentControls.data[0]["unicode"]["right"], HEIGHT//10, WIDTH//3, HEIGHT//3 + 3 * HEIGHT//128 + 3 * HEIGHT//10, textDim = True, centre = True)
                    elif p == 1:
                        p2Buttons = {
                            "up":ui.Button(currentControls.data[1]["unicode"]["up"], HEIGHT//10, 2 * WIDTH//3, HEIGHT//3, textDim = True, centre = True)
                        }
                        p2Buttons["down"] = ui.Button(currentControls.data[1]["unicode"]["down"], HEIGHT//10, 2 * WIDTH//3, HEIGHT//3 + HEIGHT//128 + HEIGHT//10, textDim = True, centre = True)
                        p2Buttons["left"] = ui.Button(currentControls.data[1]["unicode"]["left"], HEIGHT//10, 2 * WIDTH//3, HEIGHT//3 + 2 * HEIGHT//128 + 2 * HEIGHT//10, textDim = True, centre = True)
                        p2Buttons["right"] = ui.Button(currentControls.data[1]["unicode"]["right"], HEIGHT//10, 2 * WIDTH//3, HEIGHT//3 + 3 * HEIGHT//128 + 3 * HEIGHT//10, textDim = True, centre = True)

            if controls:
                if resetButton.pressed(eventQueue):
                    currentControls.reset()
                    keyReg = False
                    p1Buttons = {
                        "up":ui.Button(currentControls.data[0]["unicode"]["up"], HEIGHT//10, WIDTH//3, HEIGHT//3, textDim = True, centre = True)
                    }
                    p1Buttons["down"] = ui.Button(currentControls.data[0]["unicode"]["down"], HEIGHT//10, WIDTH//3, HEIGHT//3 + HEIGHT//128 + HEIGHT//10, textDim = True, centre = True)
                    p1Buttons["left"] = ui.Button(currentControls.data[0]["unicode"]["left"], HEIGHT//10, WIDTH//3, HEIGHT//3 + 2 * HEIGHT//128 + 2 * HEIGHT//10, textDim = True, centre = True)
                    p1Buttons["right"] = ui.Button(currentControls.data[0]["unicode"]["right"], HEIGHT//10, WIDTH//3, HEIGHT//3 + 3 * HEIGHT//128 + 3 * HEIGHT//10, textDim = True, centre = True)

                    p2Buttons = {
                        "up":ui.Button(currentControls.data[1]["unicode"]["up"], HEIGHT//10, 2 * WIDTH//3, HEIGHT//3, textDim = True, centre = True)
                    }
                    p2Buttons["down"] = ui.Button(currentControls.data[1]["unicode"]["down"], HEIGHT//10, 2 * WIDTH//3, HEIGHT//3 + HEIGHT//128 + HEIGHT//10, textDim = True, centre = True)
                    p2Buttons["left"] = ui.Button(currentControls.data[1]["unicode"]["left"], HEIGHT//10, 2 * WIDTH//3, HEIGHT//3 + 2 * HEIGHT//128 + 2 * HEIGHT//10, textDim = True, centre = True)
                    p2Buttons["right"] = ui.Button(currentControls.data[1]["unicode"]["right"], HEIGHT//10, 2 * WIDTH//3, HEIGHT//3 + 3 * HEIGHT//128 + 3 * HEIGHT//10, textDim = True, centre = True)

                for i in p1Buttons:
                    if p1Buttons[i].pressed(eventQueue):
                        keyReg = True
                        replaceKey = i
                        p = 0
            
                for i in p2Buttons:
                    if p2Buttons[i].pressed(eventQueue):
                        keyReg = True
                        replaceKey = i
                        p = 1

            if not move and slideButton.pressed(eventQueue):
                animation = Animation.Animator((WIDTH, HEIGHT), controlsBG)
                if reverse:
                    slideButton = ui.Button("<", HEIGHT//6, WIDTH//12 - WIDTH//16, HEIGHT//2 - HEIGHT//12, bg = False)
                    header = controlsFont.render("how to play", True, (255, 255, 255))
                    
                else:
                    slideButton = ui.Button(">", HEIGHT//6, WIDTH//2 + 5 * WIDTH//12, HEIGHT//2 - HEIGHT//12, bg = False)
                    header = controlsFont.render("controls", True, (255, 255, 255))
                move = True
                reverse = not reverse
                controls = reverse

            if fullbreak:
                controlsRun = False

            time.update()

        menuSheet = spritesheet.Spritesheet(pygame.transform.scale(pygame.image.load(f"./Assets/Backgrounds/mainMenuBg{random.randint(1, 4)}.png"), (WIDTH * 2, HEIGHT)))
        menuImgs = menuSheet.getSprites(WIDTH, HEIGHT, 1)[0]
        menuBg = Animation.Animator((WIDTH, HEIGHT), menuImgs, 30)

        del controlsRun, controlsBG, reverse, slideButton, move, controlsFont, header, animation

    if playButton.pressed(eventQueue):
        selectionRun = True
        selectFont = pygame.font.Font("./Assets/Fonts/pixeboy.ttf", HEIGHT//6)
        header = selectFont.render("Select track:", True, (255, 255, 255))
        currentTrack = 1
        track = pygame.transform.scale(pygame.image.load("./Assets/Backgrounds/track1.png"), (WIDTH//1.5, HEIGHT//1.5))
        startButton = ui.Button("play", HEIGHT//8, WIDTH//2 - WIDTH//10, HEIGHT - HEIGHT//32 - HEIGHT//6, WIDTH//5, HEIGHT//6)
        leftButton = ui.Button("<", HEIGHT//6, WIDTH//2 - WIDTH//8, HEIGHT - HEIGHT//32 - HEIGHT//8, bg = False)
        rightButton = ui.Button(">", HEIGHT//6, WIDTH//2 + WIDTH//8, HEIGHT - HEIGHT//32 - HEIGHT//8, bg = False)
        leftButton.textPos = (WIDTH//2 - WIDTH//8 - leftButton.txt.get_width(), HEIGHT - HEIGHT//32 - HEIGHT//8)
        leftButton.rect.x = WIDTH//2 - WIDTH//8 - leftButton.txt.get_width()

        while selectionRun:
            WIN.fill((0, 0, 0))
            WIN.blit(header, (WIDTH//2 - header.get_width()//2, HEIGHT//64))
            WIN.blit(track, (WIDTH//2 - track.get_width()//2, HEIGHT//32 + header.get_height()))

            startButton.render(WIN)
            leftButton.render(WIN)
            rightButton.render(WIN)

            pygame.display.update()

            eventQueue = pygame.event.get()

            for i in eventQueue:
                if i.type == pygame.QUIT:
                    fullbreak = True
                    break
                
                if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                    selectionRun = False
                    break
            
            if leftButton.pressed(eventQueue) and currentTrack > 1:
                currentTrack -= 1
                track = pygame.transform.scale(pygame.image.load(f"./Assets/Backgrounds/track{currentTrack}.png"), (WIDTH//1.5, HEIGHT//1.5))

            if rightButton.pressed(eventQueue) and currentTrack < 3:
                currentTrack += 1
                track = pygame.transform.scale(pygame.image.load(f"./Assets/Backgrounds/track{currentTrack}.png"), (WIDTH//1.5, HEIGHT//1.5))

            if startButton.pressed(eventQueue):
                restart = True

                while restart:
                    mainTrack = pyTrack.Track((WIDTH, HEIGHT), currentTrack)
                    gameRun = True
                    players = [player.Player((WIDTH, HEIGHT), "red"), player.Player((WIDTH, HEIGHT), "blue")]
                    paused = False
                    gameOver = False
                    time.totalTime = -5

                    if currentTrack == 1:
                        players[0].posX = WIDTH//384 * 195
                        players[0].posY = HEIGHT//216 * 168
                        players[0].rect.x =WIDTH//384 * 195
                        players[0].rect.y = HEIGHT//216 * 168
                        players[1].posX = WIDTH//384 * 195 
                        players[1].posY = HEIGHT//216 * 180
                        players[1].rect.x = WIDTH//384 * 195 
                        players[1].rect.y = HEIGHT//216 * 180
                        colour = (255, 255, 255)

                    elif currentTrack == 2:
                        players[0].posX = WIDTH//384 * 115
                        players[0].posY = HEIGHT//216 * 172
                        players[0].rect.x =WIDTH//384 * 115
                        players[0].rect.y = HEIGHT//216 * 172
                        players[1].posX = WIDTH//384 * 115
                        players[1].posY = HEIGHT//216 * 189
                        players[1].rect.x = WIDTH//384 * 115
                        players[1].rect.y = HEIGHT//216 * 189
                        colour = (255, 255, 255)

                    elif currentTrack == 3:
                        players[0].posX = WIDTH//384 * 300
                        players[0].posY = HEIGHT//216 * 181
                        players[0].rect.x = WIDTH//384 * 300
                        players[0].rect.y = HEIGHT//216 * 181
                        players[1].posX = WIDTH//384 * 300
                        players[1].posY = HEIGHT//216 * 192
                        players[1].rect.x = WIDTH//384 * 300
                        players[1].rect.y = HEIGHT//216 * 192
                        colour = (0, 0, 0)

                    while gameRun:
                        WIN.fill((0, 0, 0))
                        WIN.blit(mainTrack.img, (0, 0))

                        if time.totalTime < 0:
                            timer = menuFont.render(str(abs(time.totalTime - 1))[0], True, colour)
                            for i in players:
                                WIN.blit(i.currentImg, i.rect)

                            WIN.blit(timer, (WIDTH//2 - timer.get_width()//2, HEIGHT//2 - timer.get_height()//2))

                            for i in pygame.event.get():
                                if i.type == pygame.QUIT:
                                    fullbreak = True
                                    break

                            pygame.display.update()
                            time.update()

                            if time.totalTime + time.deltaTime >= 5:
                                del timer, colour

                            if fullbreak:
                                gameRun = False
                                break
                            continue

                        eventQueue = pygame.event.get()

                        for i in players:
                            i.move(WIN, time.deltaTime, mainTrack)

                        timeTxt = str(time.totalTime)
                        for i in range(len(timeTxt)):
                            if timeTxt[i] == ".":
                                break
                        timeTxt = timeTxt[:i+3]

                        timeImg = selectFont.render(timeTxt, True, (0, 0, 0), (255, 255, 255))
                        WIN.blit(timeImg, (WIDTH//2 - timeImg.get_width()//2, 0))

                        WIN.blit(players[0].lapsImg, (WIDTH//2 - timeImg.get_width()//2 - players[0].lapsImg.get_width(), 0))
                        WIN.blit(players[1].lapsImg, (WIDTH//2 + timeImg.get_width()//2, 0))

                        for i in players:
                            if i.win:
                                gameOver = True

                        pygame.display.update()

                        for i in eventQueue:
                            if i.type == pygame.QUIT:
                                fullbreak = True
                                break
                            elif i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                                paused = True
                                break

                        if paused:
                            pauseTxt = menuFont.render("paused", True, (255, 255, 255))
                            overlay = pygame.transform.scale(pygame.image.load("./Assets/Backgrounds/overlay.png"), (WIDTH, HEIGHT)).convert_alpha()
                            resumeButton = ui.Button("resume", HEIGHT//10, WIDTH//2 - WIDTH//12, HEIGHT//2 + HEIGHT//36, WIDTH//6, HEIGHT//10)
                            menuButton = ui.Button("menu", HEIGHT//10, WIDTH//2 - WIDTH//12, HEIGHT//2 + 2 * HEIGHT//36 + HEIGHT//10, WIDTH//6, HEIGHT//10)

                            while paused:
                                WIN.fill((0, 0, 0))
                                WIN.blit(mainTrack.img, (0, 0))

                                for i in players:
                                    WIN.blit(i.currentImg, i.rect)

                                WIN.blit(overlay, (0, 0))
                                WIN.blit(pauseTxt, (WIDTH//2 - pauseTxt.get_width()//2, HEIGHT//2 - pauseTxt.get_height()))

                                resumeButton.render(WIN)
                                menuButton.render(WIN)

                                pygame.display.update()

                                eventQueue = pygame.event.get()

                                for i in eventQueue:
                                    if i.type == pygame.QUIT:
                                        fullbreak = True
                                        break
                                    elif i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                                        paused = False
                                        break

                                if resumeButton.pressed(eventQueue):
                                    paused = False

                                if menuButton.pressed(eventQueue):
                                    backToMenu = True

                                time.update()

                                if fullbreak or backToMenu:
                                    paused = False
                                    restart = False

                            del pauseTxt, overlay, resumeButton, menuButton
                        
                        time.update()

                        if fullbreak or backToMenu or gameOver:
                            gameRun = False
                            restart = False

                    if fullbreak or backToMenu:
                        del mainTrack, paused, players, gameRun, timeTxt, timeImg, gameOver
                        restart = False
                        break

                    for i in players:
                        if i.win:
                            winner = i.colour
                            break
                    
                    winRun = True
                    header = menuFont.render(f"Game over!", True, (255, 255, 255))
                    trophyFont = pygame.font.Font("./Assets/Fonts/pixeboy.ttf", HEIGHT//20)

                    surface = pygame.surface.Surface((WIDTH//10, WIDTH//10)).convert_alpha()
                    trophy = pygame.transform.scale(pygame.image.load("./Assets/Win/trophy.png").convert_alpha(), (WIDTH//10, WIDTH//10))
                    winnerTxt = trophyFont.render(winner, True, "#5b4d00")
                    surface.blit(trophy, (0, 0))
                    surface.blit(winnerTxt, (WIDTH//20 - winnerTxt.get_width()//2, WIDTH//30))
                    surface = pygame.transform.rotate(surface, -30)
                    surface.set_colorkey((0, 0, 0))

                    timeFont = pygame.font.Font("./Assets/Fonts/pixeboy.ttf", HEIGHT//15)
                    timeTxt = str(time.totalTime)
                    for i in range(len(timeTxt)):
                        if timeTxt[i] == ".":
                            break
                    finalTime = timeFont.render(f"{winner} won in {timeTxt[:i+3]} seconds", True, (255, 255, 255))

                    overlay = pygame.transform.scale(pygame.image.load("./Assets/Backgrounds/overlay.png"), (WIDTH, HEIGHT)).convert_alpha()

                    restartButton = ui.Button("play again", HEIGHT//10, WIDTH//2 - WIDTH//8, HEIGHT//2, WIDTH//4, HEIGHT//10)
                    menuButton = ui.Button("menu", HEIGHT//10, WIDTH//2 - WIDTH//8, HEIGHT//2 + HEIGHT//10 + HEIGHT//64, WIDTH//4, HEIGHT//10)

                    while winRun:
                        WIN.fill((0, 0, 0))
                        WIN.blit(mainTrack.img, (0, 0))

                        for i in players:
                            WIN.blit(i.currentImg, i.rect)

                        WIN.blit(overlay, (0, 0))

                        WIN.blit(header, (WIDTH//2 - header.get_width()//2, HEIGHT//2 - 1.5 * header.get_height()))
                        WIN.blit(finalTime, (WIDTH//2 - finalTime.get_width()//2, HEIGHT//2 - 0.5 * header.get_height()))

                        WIN.blit(surface, (WIDTH//2 + header.get_width()//2 - surface.get_width()//2, HEIGHT//2 - 1.5 * header.get_height()))

                        restartButton.render(WIN)
                        menuButton.render(WIN)

                        pygame.display.update()

                        eventQueue = pygame.event.get()

                        for i in eventQueue:
                            if i.type == pygame.QUIT:
                                fullbreak = True
                                break

                        if restartButton.pressed(eventQueue):
                            winRun = False
                            header = selectFont.render("Select track:", True, (255, 255, 255))

                        if menuButton.pressed(eventQueue):
                            backToMenu = True

                        if fullbreak or backToMenu:
                            winRun = False
                            restart = False

                        time.update()

                    del mainTrack, paused, players, gameRun, timeTxt, timeImg, winRun, winner, trophy, trophyFont, overlay, winnerTxt, gameOver, restartButton, finalTime, timeFont, surface

            time.update()

            if fullbreak or backToMenu:
                selectionRun = False

        menuSheet = spritesheet.Spritesheet(pygame.transform.scale(pygame.image.load(f"./Assets/Backgrounds/mainMenuBg{random.randint(1, 4)}.png").convert(), (WIDTH * 2, HEIGHT)))
        menuImgs = menuSheet.getSprites(WIDTH, HEIGHT, 1)[0]
        menuBg = Animation.Animator((WIDTH, HEIGHT), menuImgs, 30)

        del selectionRun, track, startButton, selectFont, header, currentTrack, leftButton, rightButton

    for i in eventQueue:
        if i.type == pygame.QUIT:
            fullbreak = True
            break

    menuRun = not quitButton.pressed(eventQueue)

    if fullbreak:
        menuRun = False
    
    time.update()

pygame.quit()
