import pygame
import pyperclip
import time
import random
import math

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
OUTPUT_COLOR = (255,  155, 255)
PHRASE_COLOR = (55,  255, 55)
FONT_NUM = 1

DIMENSIONS = [1000, 550]

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

class UI:
    def __init__(self, ):
        pygame.init()
        self.screen = pygame.display.set_mode(DIMENSIONS)
        self.string = ''
        self.copied = False
        self.width = DIMENSIONS[0]
        self.height = DIMENSIONS[1]
        self.ballcolor = (255, 255, 255)
        self.sliced = [[], []]
        self.vx = 0.1
        self.vy = 0.1

    def changeBallColor(self,):
        def changeColor(color):
            t = random.randint(-3, 3) 
            if (color+t > 255):
                return color - t
            elif (color+t < 0):
                return color - t
            return color+t

        self.ballcolor = list(self.ballcolor)
        self.ballcolor[0] = changeColor(self.ballcolor[0]) 
        self.ballcolor[1] = changeColor(self.ballcolor[1]) 
        self.ballcolor[2] = changeColor(self.ballcolor[2]) 
        self.ballcolor = tuple(self.ballcolor)

    def swapVelocity(self, i, j):
        m1 = self.ballsize[i]
        m2 = self.ballsize[j]

        v1 = self.velocityx[i]
        v2 = self.velocityx[j]
        self.velocityx[i] = (2*m2*v2 + (m1-m2)*v1)/(m1+m2)
        self.velocityx[j] = (2*m1*v1 + (m2-m1)*v2)/(m1+m2)

        v1 = self.velocityy[i]
        v2 = self.velocityy[j]
        self.velocityy[i] = (2*m2*v2 + (m1-m2)*v1)/(m1+m2)
        self.velocityy[j] = (2*m1*v1 + (m2-m1)*v2)/(m1+m2)

    def antiGravity(self, i, j, d, r1, r2):
        def signOfNumber(n):
            if (n < 0):
                return -1
            return 1

        if not int(d) or int(r1+r2)/int(d) > 3 :
            return

        self.velocityx[i] = self.vx * int(r1+r2)/int(d) * -(signOfNumber(self.velocityx[j]))
        self.velocityy[i] = self.vy * int(r1+r2)/int(d) * -(signOfNumber(self.velocityy[j]))

        self.velocityx[j] = self.vx * int(r1+r2)/int(d) * (signOfNumber(self.velocityx[j]))
        self.velocityy[j] = self.vy * int(r1+r2)/int(d) * (signOfNumber(self.velocityy[j]))

    def collision(self, i, x1, y1, r1, j, x2, y2, r2):

        def overlap(l1, i):
            for e1 in l1:
                if e1 == i:
                    return True
            return False

        d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        if (d < (r1+r2) and len(self.sliced[i]) == 0 and not overlap(self.sliced[j], i)):
            self.swapVelocity(i, j)
        elif (d < (r1+r2) and len(self.sliced[j]) == 0 and not overlap(self.sliced[i], j)):
            self.swapVelocity(i, j)
        elif (d < (r1+r2) and not overlap(self.sliced[j], i)):
            self.sliced[i].append(j)
            self.sliced[j].append(i) 

            self.swapVelocity(i, j)
        elif (d < r1+r2 and overlap(self.sliced[i], j)):
              self.antiGravity(i, j, d, r1, r2)
        elif (d > r1+r2 and overlap(self.sliced[i], j)):
            self.sliced[i].remove(j) 
            self.sliced[j].remove(i)

    def bounceBall(self, ):
        for i, (x1, y1, r1) in enumerate(zip(self.ballx, self.bally, self.ballsize)):
            if random.randint(0, 100) > 70:
                self.changeBallColor() 
            pygame.draw.circle(self.screen, self.ballcolor, (x1, y1), r1)

            # Check every ball with every other if they collide
            for j, (x2, y2, r2) in enumerate(zip(self.ballx[i+1:], self.bally[i+1:], self.ballsize[i+1:])):
                other = j + i+1
                self.collision(i, x1, y1, r1, other, x2, y2, r2)

            self.ballx[i] += self.velocityx[i]
            self.bally[i] += self.velocityy[i]

            if (self.ballx[i] < 0):
                self.velocityx[i] = abs(self.velocityx[i])
            if (self.bally[i] < 0):
                self.velocityy[i] = abs(self.velocityy[i])
            if (self.ballx[i] > self.width):
                self.velocityx[i] = -abs(self.velocityx[i])
            if (self.bally[i] > self.height):
                self.velocityy[i] = -abs(self.velocityy[i])
            

        return
    
    def slice(self, i, radius, x, y):
        self.ballsize[i] = 5*radius/7
        self.sliced.append([i])
        self.sliced[i].append(len(self.sliced)-1)
        self.ballx.append(x)
        self.bally.append(y)
        self.ballsize.append(5*radius/7)
        self.velocityx.append(-self.velocityx[i])
        self.velocityy.append(-self.velocityy[i])

    def sliceRandomBall(self):
        randi = random.randint(0, len(self.ballx)-1)
        self.slice(randi, self.ballsize[randi], self.ballx[randi], self.bally[randi])

    def sliceBall(self, mouse):
        for i, (x, y, radius) in enumerate(zip(self.ballx, self.bally, self.ballsize)):
            if x+radius > mouse[0] > x and y+radius > mouse[1] > y and not len(self.sliced[i]):
                self.slice(i, radius, x, y)
                return

    def displayUI(self, ):

        print('You have 30 seconds to create your entropy!')
        start = time.time()
        now = time.time()
        running = True

        # Draw a solid blue circle in the center
        self.ballx = [250, 500]
        self.bally = [250, 500]
        self.velocityx = [self.vx, self.vx] 
        self.velocityy = [self.vy, self.vy] 
        self.ballsize = [140, 140] 

        while (now - start < 30 and running):
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.sliceRandomBall()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.sliceBall(event.pos)

            # Fill the background with white
            self.screen.fill((15, 16, 10))

            self.bounceBall()

            # Flip the display
            pygame.display.flip()

            now = time.time()
        print('\nTIME\'S UP!')

    def displayFancyString(self, string):
        self.string = string
        self.screen.fill((65, 40, 80))

        fonts = pygame.font.get_fonts()

        font = pygame.font.SysFont(fonts[FONT_NUM], 82)
        img = font.render(string, True, PHRASE_COLOR)
        self.screen.blit(img, (70, 300))

        font = pygame.font.SysFont(fonts[3], 122)
        img = font.render('TIME\'S UP!', True, OUTPUT_COLOR)
        self.screen.blit(img, (150, 60))

        font = pygame.font.SysFont(fonts[2], 32)
        img = font.render('Your keyphrase is:', True, OUTPUT_COLOR)
        self.screen.blit(img, (100, 250))

        # Run until the user asks to quit
        running = True
        while running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False


            c1 = (33, 132, 132)
            c2 = (198, 222, 222)
            c3 = (124, 86, 49)
            c4 = (0, 0, 255)
            c5 = (0, 255, 0)
            self.button(865, 325, 40, 40, c1, c2, c3, c4, c5)
            
            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()

    def button(self, x, y, w, h, c1, c2, c3, c4, c5):
        def drawRoundedRect(color):
            pygame.draw.rect(self.screen, color, pygame.Rect(x, y, w, h), 20, 14, 14, 6)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        drawRoundedRect(c1)

        smallText = pygame.font.Font("freesansbold.ttf", 10)

        if (self.copied):
            drawRoundedRect(c2)
            textSurf, textRect = text_objects('Copied!', smallText, c4)
            textRect.center = ( (x+(w/2)), (y+(h/2)) )
            self.screen.blit(textSurf, textRect)
            return

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            drawRoundedRect(c1)
            textSurf, textRect = text_objects('Copy', smallText, c5)
            textRect.center = ( (x+(w/2)), (y+(h/2)) )
            self.screen.blit(textSurf, textRect)
            if click[0] == 1 != None:
                pyperclip.copy(self.string)
                self.copied = True

                textSurf, textRect = text_objects('Copied!', smallText, c5)
                textRect.center = ( (x+(w/2)), (y+(h/2)) )
                self.screen.blit(textSurf, textRect)
                drawRoundedRect(BLUE)
                return

            textSurf, textRect = text_objects('Copy', smallText, c5)
            textRect.center = ( (x+(w/2)), (y+(h/2)) )
            self.screen.blit(textSurf, textRect)

        elif not self.copied:
            drawRoundedRect(c3)
            textSurf, textRect = text_objects('Copy', smallText, c5)
            textRect.center = ( (x+(w/2)), (y+(h/2)) )
            self.screen.blit(textSurf, textRect)
