import pygame
import time
import os.path
pygame.init()
BLACK = (0,0,0)
WHITE = (255,255,255)
WIN = pygame.display.set_mode((1000, 800))
NUM_FONT = pygame.font.SysFont('comicsans', 40)
pygame.font.init()


START_BUTTON = pygame.image.load(os.path.join('Assets','START.png')).convert_alpha()
RESET_BUTTON = pygame.image.load(os.path.join('Assets','RESET.png')).convert_alpha()

class Button:

    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):
        pos = pygame.mouse.get_pos()
        action = False
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        return action

class Grid:

    def __init__(self):
        self.grid = [
        [0,0,0,0,0,0,2,0,0],
        [0,8,0,0,0,7,0,9,0],
        [6,0,2,0,0,0,5,0,0],
        [0,7,0,0,6,0,0,0,0],
        [0,0,0,9,0,1,0,0,0],
        [0,0,0,0,2,0,0,4,0],
        [0,0,5,0,0,6,0,0,3],
        [0,9,0,4,0,0,0,7,0],
        [0,0,6,0,0,0,0,0,0]
        ]

    def check_col(self,col,num):
        for row in range(9):
            if num == self.grid[row][col]:
                return False
        return True

    def check_row(self,row,num):
        return num not in self.grid[row]

    def check_subgrid(self,row,col,num):
        for i in range(row//3*3, row//3*3+3):
            for j in range(col//3*3,col//3*3+3):
                if num == self.grid[i][j]:
                    return False
        return True

    def is_Valid(self,row,col,num):
        return self.check_col(col,num) and self.check_row(row,num) and self.check_subgrid(row,col,num)

    def solve(self,row=0,col=0):
        if row == 9:
            return True
        elif col == 9:
            return self.solve(row+1,0)
        elif self.grid[row][col] != 0:
            return self.solve(row,col+1)
        else:
            for i in range(1,10):
                if self.is_Valid(row,col,i):
                    self.grid[row][col] = i
                    #self.draw()
                    if self.solve(row,col+1):
                        return True
                    self.grid[row][col]=0
            return False

    def draw_number(self):
        for row in range(9):
            for col in range(9):
                num = self.grid[row][col]
                num_text = NUM_FONT.render(str(num),1,BLACK,WHITE)
                if num == 0:
                    continue
                else:
                    WIN.blit(num_text,(col*80+60,row*80+50))


    def draw_horizontal_lines(self):
        for i in range(9):
            if i%3==0:
                pygame.draw.line(WIN,BLACK,(30,30+i*80),(750,30+i*80),5)
            else:
                pygame.draw.line(WIN,BLACK,(30,30+i*80),(750,30+i*80))


    def draw_vertical_lines(self):
        for i in range(9):
            if i%3==0:
                pygame.draw.line(WIN,BLACK, (30+i*80,30), (30+i*80,750),5)
            else:
                pygame.draw.line(WIN, BLACK, (30 + i * 80, 30), (30 + i * 80, 750))

    def draw_rect(self):
        pygame.draw.rect(WIN,(0,0,0),pygame.Rect(30,30,720,720),5)
    def draw(self):
        WIN.fill(WHITE)
        self.draw_rect()
        self.draw_horizontal_lines()
        self.draw_vertical_lines()
        self.draw_number()
        #pygame.display.update()


def get_user_location(pos):
    x=(pos[1]-30)//80
    y=(pos[0]-30)//80
    return(x,y)

def draw_current_state(text):
    draw_text = NUM_FONT.render(text,1,BLACK)
    WIN.blit(draw_text,(800,800/2-draw_text.get_height()//2))
    pygame.display.update()

def main():
    run = True
    Sudoku = Grid()
    cell=None
    start = Button(800,200,START_BUTTON,0.5)
    reset = Button(800,600,RESET_BUTTON,0.5)
    current_state = ""


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.MOUSEBUTTONDOWN:
                if (pygame.mouse.get_pos()[1]>=30 and pygame.mouse.get_pos()[1]<720) and (
                    pygame.mouse.get_pos()[0]>=30 and pygame.mouse.get_pos()[0]<720
                ):
                    cell = get_user_location(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if cell!=None and cell[0]<=8 and cell[1]<=8:
                    if pygame.K_0 <= event.key <= pygame.K_9:
                        row, col = cell[0], cell[1]
                        cell = None
                        number = (int)(event.unicode)
                        Sudoku.grid[row][col] = number
        if start.draw():
            Sudoku.solve()
            if not Sudoku.solve():
                current_state = "Impossible"
            else:
                current_state = "Finished"

        if reset.draw():
            Sudoku.grid = [
                [0,0,0,0,0,0,0,0,0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]

        Sudoku.draw()
        start.draw()
        reset.draw()
        if current_state != "":
            draw_current_state(current_state)
            pygame.time.delay(5000)
            current_state = ""
            draw_current_state(current_state)

        pygame.display.update()



    pygame.quit()

if __name__ == "__main__":
    main()
