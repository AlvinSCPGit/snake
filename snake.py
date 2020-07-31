# -*- encoding=cp936 -*-
import pygame
import sys
import random
import math

SCREEN_X = 600
SCREEN_Y = 600

class Snake(object):
    def __init__(self):
        self.dirction = pygame.K_RIGHT
        self.body = []
        for x in range(5):
            self.addnode()
        
    def addnode(self):
        left,top = (0,0)
        if self.body:
            left,top = (self.body[0].left,self.body[0].top)
        node = pygame.Rect(left,top,25,25)
        if self.dirction == pygame.K_LEFT:
            node.left -= 25
        elif self.dirction == pygame.K_RIGHT:
            node.left += 25
        elif self.dirction == pygame.K_UP:
            node.top -= 25
        elif self.dirction == pygame.K_DOWN:
            node.top += 25
        self.body.insert(0,node)
        
    def delnode(self):
        self.body.pop()
        
    def isdead(self):
        if self.body[0].x  not in range(SCREEN_X):
            return True
        if self.body[0].y  not in range(SCREEN_Y):
            return True
        if self.body[0] in self.body[1:]:
            return True
        return False
        
    def move(self):
        self.addnode()
        self.delnode()
        
    def changedirection(self,curkey):
        LR = [pygame.K_LEFT,pygame.K_RIGHT]
        UD = [pygame.K_UP,pygame.K_DOWN]
        if curkey in LR+UD:
            if (curkey in LR) and (self.dirction in LR):
                return
            if (curkey in UD) and (self.dirction in UD):
                return
            self.dirction = curkey
       
    
class Food:
    def __init__(self):
        self.rect = pygame.Rect(-25,0,25,25)
        
    def remove(self):
        self.rect.x=-25
    
    def set(self):
        if self.rect.x == -25:
            allpos = []
            for pos in range(25,SCREEN_X-25,25):
                allpos.append(pos)
            self.rect.left = random.choice(allpos)
            self.rect.top  = random.choice(allpos)
            print(self.rect)
            

def show_text(screen, pos, text, color, font_bold = False, font_size = 60, font_italic = False):    
    cur_font = pygame.font.SysFont("Courier", font_size)  
    cur_font.set_bold(font_bold)  
    cur_font.set_italic(font_italic)  
    text_fmt = cur_font.render(text, 1, color)  
    screen.blit(text_fmt, pos)

     
def main():
    pygame.init()
    screen_size = (SCREEN_X,SCREEN_Y)
    bluezone_size = 400
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    score = 0
    signal = 100
    isdead = False
    phase_damage = [1,2,3,6,8]
    
    # 蛇/食物
    snake = Snake()
    food = Food()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                snake.changedirection(event.key)
                # 死后按space重新
                if event.key == pygame.K_SPACE and isdead:
                    return main()
                if event.key == pygame.K_r:
                    if len(snake.body) > 3:
                        snake.delnode()
                        signal += 5
                        score += 1000
                
            
        screen.fill((255,255,255))
        
        # 画蛇身 / 每一步+1分
        if not isdead:
            snake.move()
        for rect in snake.body:
            pygame.draw.rect(screen,(20,220,39),rect,0)
            
        isdead = snake.isdead()

        curphase = math.floor((400-bluezone_size)/80)
        bluezone_size -= 0.5
        bluezone_size = max(bluezone_size,100)
        if math.sqrt(
            abs(snake.body[0].x-300)**2+
            abs(snake.body[1].y-300)**2) > bluezone_size+25:
            show_text(screen, (270,125), 'Bluezone countdown',[255,0,0],False,20)
            show_text(screen, (270,150), '%.1f'%(signal/phase_damage[curphase]/10),[255,0,0],False,50)
            signal -= phase_damage[curphase]
        pygame.draw.circle(screen, [0,0,255],[300,300],int(bluezone_size),2)
        
        if signal <= 0:
            isdead = True
            signal = 0
        if isdead:
            show_text(screen,(100,200),'YOU DEAD!',(227,29,18),False,100)
            show_text(screen,(150,260),'press space to try again...',(0,0,22),False,30)
        show_text(screen,(25,120),'PHASE %d'%(curphase+1),(255,0,0),True,40)
        
        show_text(screen,(25,25), 'TOTAL: ',(0,0,0),True,40)
        show_text(screen,(200,25), '%dPTS'%score, (0,0,255),True,40)
        
        if food.rect == snake.body[0]:
            score += 500
            signal += 10
            signal = min(signal,100)
            food.remove()
            snake.addnode()
        
        # 食物投递
        food.set()
        pygame.draw.rect(screen,(136,0,21),food.rect,0)
        
        pygame.display.update()
        clock.tick(10)
    
    
if __name__ == '__main__':
    main()
