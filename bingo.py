import pygame
import random
import os
import time
import playsound
pygame.font.init()

CUBE_SIZE = 90
MARGIN_SIZE = 1
WIDTH,HEIGHT = CUBE_SIZE * 5 + MARGIN_SIZE*4,CUBE_SIZE * 7 + MARGIN_SIZE * 5
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("  Bingo @Advait")

# Loading Images
CROSS = pygame.image.load(os.path.join("assets","cross.png"))
SLASH_BLUE = pygame.image.load(os.path.join("assets","slash_blue.png"))
SLASH_GREEN = pygame.image.load(os.path.join("assets","slash_green.png"))

# Loading Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))

# Loading Icon Image
ICON = pygame.image.load(os.path.join("assets","icon.png"))
pygame.display.set_icon(ICON)


# Different Font Labels used
main_font = pygame.font.SysFont("comicsans",87)
digit_font = pygame.font.SysFont("comicsans",45)
statement_font = pygame.font.SysFont("comicsans",40)
title_font = pygame.font.SysFont("comicsans",60)
name_font = pygame.font.SysFont("comicsans",40)



class Digit:                                # From printing the digit in the blank grid
    def __init__(self,count_lable,x,y):
        self.count_lable = count_lable
        self.x = x
        self.y = y

    def draw(self,window):
        window.blit(self.count_lable,(self.x,self.y))


class Crossed_Digit:                        # For cutting the digits and BINGO alphabets in the filled grid 
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img

    def draw(self,window):
        window.blit(self.img,(self.x+20,self.y+20))


class STATEMENT_PANEL:
    def __init__(self,text):
        self.text = text

    def draw(self,window):
        statement = statement_font.render(f"{self.text}",1,(255,255,255))
        WIN.blit(statement,(WIDTH//2 - statement.get_width()//2,(CUBE_SIZE + MARGIN_SIZE)* 6 + 30))
        


def check_for_winner(winner,grid,bot,crossed_digits,no_of_bingo_cuts,grid_bingo,bot_bingo):
  
    grid_count = 0
    bot_count = 0

    for i in range(5):              # checks the rows
        if(grid[i][0] == grid[i][1] == grid[i][2] == grid[i][3] == grid[i][4] == "X"):
            grid_count+=1

        if(bot[i][0] == bot[i][1] == bot[i][2] == bot[i][3] == bot[i][4] == "O"):
            bot_count+=1

    for i in range(5):              # checks the columns
        if(grid[0][i] == grid[1][i] == grid[2][i] == grid[3][i] == grid[4][i] == "X"):
            grid_count+=1

        if(bot[0][i] == bot[1][i] == bot[2][i] == bot[3][i] == bot[4][i] == "O"):
            bot_count+=1                

    if(grid[0][0] == grid[1][1] == grid[2][2] == grid[3][3] == grid[4][4] == "X"):  #checks the first diagonal
        grid_count+=1
    
    if(grid[0][4] == grid[1][3] == grid[2][2] == grid[3][1] == grid[4][0] == "X"):  #checks the second diagonal
        grid_count += 1

    if(bot[0][0] == bot[1][1] == bot[2][2] == bot[3][3] == bot[4][4] == "O"):       #checks the first diagonal
        bot_count+=1
    
    if(bot[0][4] == bot[1][3] == bot[2][2] == bot[3][1] == bot[4][0] == "O"):       #checks the first diagonal
        bot_count += 1

    grid_bingo = grid_count
    bot_bingo = bot_count

    if bot_bingo < 5:       # if game still going on
        for i in range(no_of_bingo_cuts,grid_bingo):        #adding only the new crosses in the list (leaving the previous ones)
            playsound.playsound("Soundtracks/pressed.mp3",False)
            cross_digits = Crossed_Digit(i * (CUBE_SIZE + MARGIN_SIZE),CUBE_SIZE*5 + MARGIN_SIZE * 5,CROSS)
            crossed_digits.append(cross_digits)
              
    no_of_bingo_cuts = grid_bingo            

    if bot_count >= 5:
        print("BOT WINNER")
        winner = "BOT"

    elif grid_count >= 5:
        winner = "You"
        print("HUMAN WINNER")
 
    return winner,grid,bot,crossed_digits,no_of_bingo_cuts,grid_bingo,bot_bingo


def flip_player(bot,grid,crossed_digits,statement_panel,bot_random,winner,no_of_bingo_cuts,grid_bingo,bot_bingo):

    pos = []    #used for storing the x and y coordinates of the element to be deleted from the grid

    random_choice = random.choice(bot_random)       # Randomly chosing a digit from the bot's bingo grid
    bot_random.remove(random_choice)                    # and deleting it so that it can't be chosen twice :p

    stat = STATEMENT_PANEL(f"BOT selected : {random_choice}")
    statement_panel.clear()
    statement_panel.append(stat)

    for i in range(5):              # for finding the x and y coordinates in the Human's grid
        for j in range(5):
            if grid[i][j] == random_choice:
                pos = [i,j]
                break

    bot = [[p if p != random_choice else "O" for p in s] for s in bot]  # cutting the selected digit from the bot's grid

    winner,grid,bot,crossed_digits,no_of_bingo_cuts,grid_bingo,bot_bingo = check_for_winner(winner,grid,bot,crossed_digits,no_of_bingo_cuts,grid_bingo,bot_bingo)

    grid = [[p if p != random_choice else "X" for p in s] for s in grid]    # cutting the selected digit from the bot's grid

    x1 = pos[1]*(CUBE_SIZE+MARGIN_SIZE)
    y1 = pos[0]*(CUBE_SIZE+MARGIN_SIZE)

    cross_digit = Crossed_Digit(x1,y1,SLASH_BLUE)
    crossed_digits.append(cross_digit)       
         
    return bot,grid,crossed_digits,statement_panel,bot_random,winner,no_of_bingo_cuts,grid_bingo,bot_bingo


def main():
    time.sleep(0.2)
    run = True

    grid = []           # User's grid to be filled by the user
    for row in range(5):
        grid.append([])
        for column in range(5):
            grid[row].append(0)

    solver = []         # An auxillary grid only used for filling the digits
    for row in range(5):
        solver.append([])
        for column in range(5):
            solver[row].append("-")

    game_is_still_going = True
    winner = None
    grid_bingo = 0
    bot_bingo = 0
    digits = []
    crossed_digits = []
    statement_panel = []
    no_of_bingo_cuts = 0

    bot = []            #Bot's grid whose value is assigned randomly

    # Assigning Random values to the BOT's grid
    bot_random = random.sample(range(1,26),25)
    w = 0
    for i in range(5):
        bot.append(bot_random[w:w+5])
        w+=5
       
    lost_count = 0      # after the gameover keeping track of number of seconds
    count = 0           # counts which digit to be entered in the grid, value incremented when the mouse is pressed

    clock = pygame.time.Clock()


    def redraw_window():

        WIN.fill((255,255,255))         # WHITE BACKGROUND
        for i in range(6):              # The GRIDS
            for j in range(6):
                pygame.draw.rect(WIN,(0,0,0),(j*CUBE_SIZE+j*MARGIN_SIZE,i*CUBE_SIZE+i*MARGIN_SIZE,CUBE_SIZE,CUBE_SIZE))

        pygame.draw.rect(WIN,(0,0,0),(0,(j+1)*CUBE_SIZE+j*MARGIN_SIZE,CUBE_SIZE*6 + MARGIN_SIZE * 5,CUBE_SIZE))  # The STATEMENT Panel

        B = main_font.render("B",1,(241,168,197))
        I = main_font.render("I",1,(241,168,197))
        N = main_font.render("N",1,(241,168,197))
        G = main_font.render("G",1,(241,168,197))
        O = main_font.render("O",1,(241,168,197))
        WIN.blit(B,(0*(CUBE_SIZE + MARGIN_SIZE)+25,(CUBE_SIZE + MARGIN_SIZE) * 5 + 20))
        WIN.blit(I,(1*(CUBE_SIZE + MARGIN_SIZE)+35,(CUBE_SIZE + MARGIN_SIZE) * 5 + 20))
        WIN.blit(N,(2*(CUBE_SIZE + MARGIN_SIZE)+25,(CUBE_SIZE + MARGIN_SIZE) * 5 + 20))
        WIN.blit(G,(3*(CUBE_SIZE + MARGIN_SIZE)+25,(CUBE_SIZE + MARGIN_SIZE) * 5 + 20))
        WIN.blit(O,(4*(CUBE_SIZE + MARGIN_SIZE)+25,(CUBE_SIZE + MARGIN_SIZE) * 5 + 20))
        pygame.draw.rect(WIN,(255,255,255),(0,6*(CUBE_SIZE+MARGIN_SIZE),WIDTH,MARGIN_SIZE))


        for digit in digits:                    #draws all the digits
            digit.draw(WIN)

        
        for cross in crossed_digits:            #crossed all the digits  
            cross.draw(WIN)

        for stat in statement_panel:            #prints the statements
            stat.draw(WIN) 

        if winner != None:
            lost_lable = main_font.render(f"{winner} Won",1,(255,255,255))
            pygame.draw.rect(WIN,(0,0,0),(WIDTH//2 - lost_lable.get_width()//2,HEIGHT//3,lost_lable.get_width() + 20,lost_lable.get_height()+10))
            WIN.blit(lost_lable,(WIDTH//2 - lost_lable.get_width()//2 + 5,HEIGHT//3 + 5) )     
         

        pygame.display.update()

    while run :
        clock.tick(60)
        redraw_window()

        if(winner != None):
            game_is_still_going = False
            lost_count +=1

        if game_is_still_going == False:
            if lost_count > 60*4:
                run = False
            else:
                continue
   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run = False

            elif count <= 24 and event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position

                pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates

                column = pos[0] // (CUBE_SIZE + MARGIN_SIZE//2)     # x coordinate
                row = pos[1] // (CUBE_SIZE + MARGIN_SIZE//2)        # y coordinate

                if(row<5 and column<5 and grid[row][column] == 0):
                    count+=1
                    grid[row][column] = count
                    str_count = str(count)
                    count_lable = digit_font.render(str_count,1,(255,255,255))
                    
                    x = column*(CUBE_SIZE+MARGIN_SIZE)+43 - count_lable.get_width()//2
                    y = row*(CUBE_SIZE+MARGIN_SIZE)+35

                    stat = STATEMENT_PANEL(f"You assigned : {count}")
                    statement_panel.clear()
                    statement_panel.append(stat)


                    if count == 25:
                        stat = STATEMENT_PANEL(f"Let's Start !")
                        statement_panel.clear()
                        statement_panel.append(stat)


                    digit = Digit(count_lable,x,y)
                    digits.append(digit)


            elif count == 25 and event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position

                pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates

                column1 = pos[0] // (CUBE_SIZE + MARGIN_SIZE//2)
                row1 = pos[1] // (CUBE_SIZE + MARGIN_SIZE//2)

                if(row1<5 and column1<5 and solver[row1][column1] == "-" ):
                    
                    solver_del = grid[row1][column1]
                    if(solver_del not in bot_random):
                        continue
                    grid[row1][column1] = "X"
                    bot = [[p if p != solver_del else "O" for p in s] for s in bot]
                    bot_random.remove(solver_del)

                    #print("GRID - ",grid)
                    #print("BOT -",bot)
                    x1 = column1*(CUBE_SIZE+MARGIN_SIZE) - count_lable.get_width()//2
                    y1 = row1*(CUBE_SIZE+MARGIN_SIZE)

                    cross_digit = Crossed_Digit(x1+10,y1,SLASH_GREEN)
                    crossed_digits.append(cross_digit)
                    
                    bot,grid,crossed_digits,statement_panel,bot_random,winner,no_of_bingo_cuts,grid_bingo,bot_bingo = flip_player(bot,grid,crossed_digits,statement_panel,bot_random,winner,no_of_bingo_cuts,grid_bingo,bot_bingo)

                
        winner,grid,bot,crossed_digits,no_of_bingo_cuts,grid_bingo,bot_bingo = check_for_winner(winner,grid,bot,crossed_digits,no_of_bingo_cuts,grid_bingo,bot_bingo)
        


def main_menu():

    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_lable = title_font.render("Click here to begin..",1,(255,255,255))
        my_name = statement_font.render("- Advait Shrivastava",1,(255,255,255))
        WIN.blit(title_lable,(WIDTH//2 - title_lable.get_width()//2,HEIGHT//3))
        WIN.blit(my_name,(WIDTH - my_name.get_width() - 20,HEIGHT - HEIGHT//3))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

                

main_menu()


