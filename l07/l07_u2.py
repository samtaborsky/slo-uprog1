from tkinter import *
import time
import random
import threading
import os
import sys

n = 20
started = False
d = 'e'
snake_def = [[0, 0], [0, 1], [0, 2]]
speed = 0.5


def run():
    thread = threading.Thread(target=move)
    thread.start()


def change_e(*args):
    global d
    d = 'e'


def change_w(*args):
    global d
    d = 'w'


def change_n(*args):
    global d
    d = 'n'


def change_s(*args):
    global d
    d = 's'


def move():
    global speed
    snake = snake_def[:]
    for x in range(len(snake)):
        matrix[snake[x][0]][snake[x][1]]['bg'] = 'blue'
    gen_food(snake)
    time.sleep(speed)

    while started:
        new_row = 0
        new_col = 0
        if d == 'e':
            new_row = snake[-1][0]
            new_col = snake[-1][1] + 1
            if new_col == n:
                new_col = 0
        elif d == 'w':
            new_row = snake[-1][0]
            new_col = snake[-1][1] - 1
            if new_col == -1:
                new_col = n - 1
        elif d == 's':
            new_row = snake[-1][0] + 1
            new_col = snake[-1][1]
            if new_row == n:
                new_row = 0
        elif d == 'n':
            new_row = snake[-1][0] - 1
            new_col = snake[-1][1]
            if new_row == -1:
                new_row = n - 1

        if vyhodnot(new_row, new_col) == 1:
            gen_food(snake)
            if speed > 0.05:
                speed -= 0.05
        else:
            matrix[snake[0][0]][snake[0][1]]['bg'] = 'white'
            del snake[0]
        snake.append([new_row, new_col])
        if vyhodnot(snake) == 2:
            startlabel['text'] = 'SMRT'
            break
        else:
            matrix[snake[-1][0]][snake[-1][1]]['bg'] = 'blue'

        if vyhodnot(snake) == 3:
            startlabel['text'] = 'VYHRA'
            break
        time.sleep(speed)


def gen_food(s):
    food_row = random.randint(0, n - 1)
    while abs(s[-1][0] - food_row) <= 2:
        food_row = random.randint(0, n - 1)
    food_col = random.randint(0, n - 1)
    while abs(s[-1][1] - food_col) <= 2:
        food_col = random.randint(0, n - 1)
    if matrix[food_row][food_col]['bg'] == 'blue':
        gen_food(s)
    else:
        matrix[food_row][food_col]['bg'] = 'green'


# noinspection PyTypeChecker
def vyhodnot(*args):
    if len(args) == 1:
        if matrix[args[0][-1][0]][args[0][-1][1]]['bg'] == 'blue':
            return 2
        if len(args[0]) == n*n:
            return 3
    elif len(args) == 2:
        if matrix[args[0]][args[1]]['bg'] == 'green':
            return 1


def startstop():
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


def kill(*args):
    if started:
        startstop()
    root.destroy()


root = Tk()
path = os.path.dirname(__file__) + r'\snake.ico'
root.iconbitmap(path)
root.title('Snake')
root.geometry('500x500')
root.option_add('*Font', 'Verdana 14')
root.focus()

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
sys.exit()
