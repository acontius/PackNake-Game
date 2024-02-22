import curses
import random
import time
import sys
import select


#setting
testng = False
food_age = 500
food_number = 10
player_char = '🚙'
food_cahr = '🥫'
enemy_char = '💣'
barrier_char = '𝌉'


def get_key():
    while True:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        else:
            return ''


stdscr = curses.initscr() #openning a screen
curses.noecho() # we use no echo to dont see every thing we entered in the terminal!
curses.cbreak() # doesn't need enter after every everything
stdscr.keypad(True)
stdscr.nodelay(True)

curses.curs_set(False)

maxl = curses.LINES - 1
maxc = curses.COLS - 1

score = 0
world = []
food = []
enemy = []

player_c = player_l = 1


def random_place():
    a = random.randint(0, maxl - 1)
    b = random.randint(0, maxc - 1)
    while world[a][b] != ' ':
        a = random.randint(0, maxl - 1)
        b = random.randint(0, maxc - 1)
    return a, b

def init(): #creating game's world
    global player_l , player_c 
    for i in range (-1 , maxl + 1):
        world.append([])
        for j in range(-1 ,maxc + 1):
            world[i].append(' ' if random.randint(0, 100) > 0.03 else barrier_char) # adding Barriers
    
    for i in range(food_number):
        food_l , food_c = random_place()
        food_age = random.randint(1000 , 10000)
        food.append((food_l,food_c,food_age))
    for i in range(10):
        enemy_l,enemy_c = random_place()
        enemy.append((enemy_l,enemy_c))

def in_range(a, min , max):
    if a > max :
        return max
    if a < min :
        return max
    return a

    player_l , player_c = random_place()

#printing the whole world
def draw():
    for i in range(maxl):
        for j in range(maxc):
            stdscr.addch(i , j , world[i][j])
    stdscr.addstr(0 , 0 , f"Score = {score}")

#showing the food
    for f in food :
        food_l ,food_c , food_age = f
        stdscr.addch(food_l , food_c , food_cahr)

#showing the enemy 
    for e in enemy:
        l , c = e
        stdscr.addch(l ,c , enemy_char)

#showing the player
        stdscr.addch(player_l , player_c , player_char)
        stdscr.refresh()

def move(c):
    global player_c,player_l
    '''get one of the asdw and move toward that direction'''
    if c == 'w' and world[player_l - 1][player_c] != barrier_char:
        player_l -= 1
    elif c == 's' and world[player_l + 1][player_c] != barrier_char:
        player_l += 1
    if c == 'a' and world[player_l][player_c - 1] != barrier_char:
        player_c -= 1
    elif c == 'd' and world[player_l][player_c + 1] != barrier_char:
        player_c += 1

    player_l = in_range(player_l , 0 , maxl - 1)
    player_c = in_range(player_c , 0 , maxc - 1)
        

def check_food():
    global score
    for i in range(len(food)) :
        food_l , food_c , food_age = food[i]
        food_age -= 1
        if food_l == player_l and food_c == player_c :
            score += 10
            food_l , food_c = random_place()
            food_age = random.randint(1000 ,10000)
        if food_age <= 0 : 
            food_l , food_c = random_place()
            food_age = random.randint(food_number,food_number*5)
        food[i] = (food_l,food_c,food_age)



def move_enemy():
    for i in range(len(enemy)):
        l , c = enemy[i]
        if random.random() > 0.5 :
            if l > player_l:
                l -= 1
        if random.random() > 0.5 :        
            if c > player_c:
              c -= 1
        if random.random() > 0.5 :      
            if l < player_l:
              l += 1
        if random.random() > 0.5 :      
            if c < player_c:
                c += 1
            l += random.choice([0 , 1 , -1])
            c += random.choice([0 , 1 , -1])
            l = in_range(l , 0 , maxl)
            c = in_range(c , 0 , maxc)

            enemy[i] = (l , c)

    if l == player_l and c == player_c :
        stdscr.addstr(maxl//2, maxc//2, "Cyka Blyat! You Died Nakhoy!")
        stdscr.refresh()
        time.sleep(3)
        playing = False

init()
playing = True
while playing:
    try:
        c = stdscr.getkey()
    except curses.error:
        c = ''
    if c in "asdw":
        move(c)
    elif c == 'q':
        playing = False
    check_food()
    move_enemy()
    time.sleep(0.05)
    
    draw()

stdscr.addstr(maxl//2,maxc//2,"Thanks for playing!")
stdscr.refresh()
time.sleep(2)
stdscr.clear()
stdscr.refresh()
