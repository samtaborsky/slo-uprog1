import os
import random
import threading
import time
from tkinter import *


n = 20
started = False
d = 'e'  # smer (east, west, north, south)
snake_def = [[0, 0], [0, 1], [0, 2]]  # zakladny had, moze byt lubovolne upraveny (chvost: [0], hlava: [-1])
speed = 0.5


def run():
    """Start pohyboveho vlakna"""
    thread = threading.Thread(target=move)
    thread.start()


def change_e(*args):
    """Zmena smeru doprava"""
    global d
    d = 'e'


def change_w(*args):
    """Zmena smeru dolava"""
    global d
    d = 'w'


def change_n(*args):
    """Zmena smeru hore"""
    global d
    d = 'n'


def change_s(*args):
    """Zmena smeru dole"""
    global d
    d = 's'


def move():
    """Kompletna obsluha hada, pohyb, jedenie, smrt..."""
    global speed
    snake = snake_def[:]
    for x in range(len(snake)):  # vykreslenie zakladneho hada
        matrix[snake[x][0]][snake[x][1]]['bg'] = 'blue'
    gen_food(snake)
    time.sleep(speed)

    while started:
        new_row = 0
        new_col = 0
        if d == 'e':  # pohyb doprava
            new_row = snake[-1][0]
            new_col = snake[-1][1] + 1
            if new_col == n:
                new_col = 0
        elif d == 'w':  # pohyb dolava
            new_row = snake[-1][0]
            new_col = snake[-1][1] - 1
            if new_col == -1:
                new_col = n - 1
        elif d == 's':  # pohyb dole
            new_row = snake[-1][0] + 1
            new_col = snake[-1][1]
            if new_row == n:
                new_row = 0
        elif d == 'n':  # pohyb hore
            new_row = snake[-1][0] - 1
            new_col = snake[-1][1]
            if new_row == -1:
                new_row = n - 1

        if vyhodnot(new_row, new_col) == 1:  # pokial dalsie policko obsahuje jedlo
            gen_food(snake)
            if speed > 0.05:  # po tejto hodnote to uz bolo neovladatelne
                speed -= 0.025
        else:  # posunutie chvostu
            matrix[snake[0][0]][snake[0][1]]['bg'] = 'white'
            del snake[0]
        snake.append([new_row, new_col])
        if vyhodnot(snake) == 2:  # pokial dalsie policko obsahuje cast hada
            startlabel['text'] = 'SMRT'
            break
        else:
            matrix[snake[-1][0]][snake[-1][1]]['bg'] = 'blue'

        if vyhodnot(snake) == 3:  # pokial vsetky policka obsahuju hada
            startlabel['text'] = 'VYHRA'
            break
        time.sleep(speed)


def gen_food(s):  # TODO generovanie jedla ak je had velmi dlhy
    """Generovanie jedla"""
    food_row = random.randint(0, n - 1)
    while abs(s[-1][0] - food_row) <= 2:  # podmienky aby jedlo nebolo prilis blizko hada
        food_row = random.randint(0, n - 1)
    food_col = random.randint(0, n - 1)
    while abs(s[-1][1] - food_col) <= 2:
        food_col = random.randint(0, n - 1)
    if matrix[food_row][food_col]['bg'] == 'blue':  # podmienka aby jedlo nebolo vnutri hada
        gen_food(s)
    else:
        matrix[food_row][food_col]['bg'] = 'green'


# noinspection PyTypeChecker
def vyhodnot(*args):
    """Vyhodnotenie stavu hlavy/hada
            Arguments:
                *args:
                    snake (list): matica s poziciami hada
                    new_row (int): nova riadkova pozicia hlavy
                    new_col (int): nova stlpcova pozicia hlavy

            Returns:
                int: stav (1/2/3)
    """

    if len(args) == 1:  # SMRT
        if matrix[args[0][-1][0]][args[0][-1][1]]['bg'] == 'blue':
            return 2
        if len(args[0]) == n*n:  # VYHRA
            return 3
    elif len(args) == 2:  # zjedenie jedla
        if matrix[args[0]][args[1]]['bg'] == 'green':
            return 1


def startstop():
    """Nastartovanie a stopnutie a reset programu"""
    global started, d, speed
    if not started:
        started = True
        startbutton['text'] = 'RESET'
        startbutton['bg'] = 'red'
        startlabel['text'] = ' '
        run()
    elif started:
        started = False
        d = 'e'
        speed = 0.5
        startbutton['text'] = 'START'
        startbutton['bg'] = 'green'
        startlabel['text'] = 'Klikni...'
        for x in range(n):
            for y in range(n):
                matrix[x][y]['bg'] = 'white'


def kill(*args):  # pokial bezal thread, boli problemy so zatvorenim procesu, osetril som to takymto sposobom
    if started:
        startstop()
    root.destroy()


# okno a jeho parametre
root = Tk()
path = os.path.dirname(__file__) + r'\snake.ico'
root.iconbitmap(path)
root.title('Snake')
root.geometry('500x500')
root.option_add('*Font', 'Verdana 14')
root.focus()

# vygenerovanie matice tlacidiel
matrix = []
for i in range(n):
    matrix.append([])
    root.rowconfigure(i, weight=1)
    for j in range(n):
        root.columnconfigure(j, weight=1)
        b = Button(root, text=' ', bg='white')
        b.grid(row=i, column=j, sticky='NSEW')
        b['state'] = DISABLED
        matrix[i].append(b)

startlabel = Label(root, text='Klikni...')
startbutton = Button(root, text='START', bg='green', command=startstop)
startlabel.grid(row=n+1, columnspan=n)
startbutton.grid(row=n+2, column=0, columnspan=n)
root.bind('<Right>', change_e)
root.bind('<Left>', change_w)
root.bind('<Up>', change_n)
root.bind('<Down>', change_s)
root.bind('<Escape>', kill)
root.protocol('WM_DELETE_WINDOW', kill)
root.mainloop()
