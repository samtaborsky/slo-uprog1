import configparser
import logging
import os
import random
import threading
import time
from tkinter import *

path = os.path.dirname(__file__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)-9s - %(message)s')

config = configparser.ConfigParser()
config.read(path + r'\hasici.ini')
logging.info(f'Reading the configuration file {path}\hasici.ini ...')
background_color = config['VALUES']['background_color']
fire_color = config['VALUES']['fire_color']
fire_speed = int(config['VALUES']['fire_speed'])
firemen_speed = int(config['VALUES']['firemen_speed'])
time.sleep(0.1)
logging.info('Configuration file read!')

directions = ['n', 's', 'w', 'e']
lock = threading.Lock()
started = False


def burn(lck=lock):
    """Control of burning"""
    global fire
    time.sleep(fire_speed)
    while started:
        next_fire = []
        lck.acquire()
        # logging.debug('burn acquired lock')

        for x in fire:
            next_right = [x[0], x[1] + 1]
            if matrix[x[0]][x[1] + 1]['bg'] == background_color:
                if next_right not in next_fire:
                    next_fire.append(next_right)
            next_left = [x[0], x[1] - 1]
            if matrix[x[0]][x[1] - 1]['bg'] == background_color:
                if next_left not in next_fire:
                    next_fire.append(next_left)
            next_up = [x[0] - 1, x[1]]
            if matrix[x[0] - 1][x[1]]['bg'] == background_color:
                if next_up not in next_fire:
                    next_fire.append(next_up)
            next_down = [x[0] + 1, x[1]]
            if matrix[x[0] + 1][x[1]]['bg'] == background_color:
                if next_down not in next_fire:
                    next_fire.append(next_down)
        # logging.debug(next_fire)
        for x in next_fire:
            if len(firemen) == 0:
                fire.append(x)
                matrix[x[0]][x[1]]['text'] = '@'
                matrix[x[0]][x[1]]['bg'] = fire_color
            for w in range(len(behind_firemen)):
                if x not in behind_firemen[w]:
                    fire.append(x)
                    matrix[x[0]][x[1]]['text'] = '@'
                    matrix[x[0]][x[1]]['bg'] = fire_color

        lck.release()
        # logging.debug('burn released lock')
        time.sleep(fire_speed)


def check_fire_distance(direction, fire_pos, position):
    """Check the distance of a fireman from a specific fire"""
    if direction == 'n':
        return position[0] - fire_pos[0]
    elif direction == 's':
        return fire_pos[0] - position[0]
    elif direction == 'w':
        return position[1] - fire_pos[1]
    elif direction == 'e':
        return fire_pos[1] - position[1]


def count_free_btns(pos):
    """Count how many free buttons are in each direction to move"""
    direction_dict = {}
    closest_fire_dict = {}
    for x in directions:
        found_fire_flag = False
        free_btns = 0
        if x == 'n':
            rows_n = pos[0] - 1
            for y in range(rows_n):
                if matrix[rows_n - y][pos[1]]['text'] == ' ':
                    free_btns += 1
                elif matrix[rows_n - y][pos[1]]['text'] == '@':
                    free_btns += 1
                    if not found_fire_flag:
                        closest_fire_dict[x] = [rows_n - y, pos[1]]
                        found_fire_flag = True
                elif matrix[rows_n - y][pos[1]]['text'] == '#':
                    break
                elif matrix[rows_n - y][pos[1]]['bg'] == 'blue':
                    free_btns += 1
            direction_dict[x] = free_btns
        elif x == 's':
            rows_s = len(matrix) - 2 - pos[0]
            for y in range(rows_s):
                if matrix[pos[0] + 1 + y][pos[1]]['text'] == ' ':
                    free_btns += 1
                elif matrix[pos[0] + 1 + y][pos[1]]['text'] == '@':
                    free_btns += 1
                    if not found_fire_flag:
                        closest_fire_dict[x] = [pos[0] + 1 + y, pos[1]]
                        found_fire_flag = True
                elif matrix[pos[0] + 1 + y][pos[1]]['text'] == '#':
                    break
                elif matrix[pos[0] + 1 + y][pos[1]]['bg'] == 'blue':
                    free_btns += 1
            direction_dict[x] = free_btns
        elif x == 'w':
            columns_w = pos[1] - 1
            for y in range(columns_w):
                if matrix[pos[0]][columns_w - y]['text'] == ' ':
                    free_btns += 1
                elif matrix[pos[0]][columns_w - y]['text'] == '@':
                    free_btns += 1
                    if not found_fire_flag:
                        closest_fire_dict[x] = [pos[0], columns_w - y]
                        found_fire_flag = True
                elif matrix[pos[0]][columns_w - y]['text'] == '#':
                    break
                elif matrix[pos[0]][columns_w - y]['bg'] == 'blue':
                    free_btns += 1
            direction_dict[x] = free_btns
        elif x == 'e':
            columns_e = len(matrix[0]) - 2 - pos[1]
            for y in range(columns_e):
                if matrix[pos[0]][pos[1] + 1 + y]['text'] == ' ':
                    free_btns += 1
                elif matrix[pos[0]][pos[1] + 1 + y]['text'] == '@':
                    free_btns += 1
                    if not found_fire_flag:
                        closest_fire_dict[x] = [pos[0], pos[1] + 1 + y]
                        found_fire_flag = True
                elif matrix[pos[0]][pos[1] + 1 + y]['text'] == '#':
                    break
                elif matrix[pos[0]][pos[1] + 1 + y]['bg'] == 'blue':
                    free_btns += 1
            direction_dict[x] = free_btns
    return [direction_dict, closest_fire_dict]


def extinguish(rpos, cpos, lck=lock):
    """Extinguish a 3x3 field around user input"""
    global fire
    lck.acquire()
    # logging.info('acquired lock')

    if matrix[rpos][cpos]['text'] == '@':
        matrix[rpos][cpos]['text'] = ' '
        matrix[rpos][cpos]['bg'] = 'white'
        fire.remove([rpos, cpos])

    if matrix[rpos + 1][cpos]['text'] == '@':
        matrix[rpos + 1][cpos]['text'] = ' '
        matrix[rpos + 1][cpos]['bg'] = 'white'
        fire.remove([rpos + 1, cpos])

    if matrix[rpos - 1][cpos]['text'] == '@':
        matrix[rpos - 1][cpos]['text'] = ' '
        matrix[rpos - 1][cpos]['bg'] = 'white'
        fire.remove([rpos - 1, cpos])

    if matrix[rpos][cpos + 1]['text'] == '@':
        matrix[rpos][cpos + 1]['text'] = ' '
        matrix[rpos][cpos + 1]['bg'] = 'white'
        fire.remove([rpos, cpos + 1])

    if matrix[rpos][cpos - 1]['text'] == '@':
        matrix[rpos][cpos - 1]['text'] = ' '
        matrix[rpos][cpos - 1]['bg'] = 'white'
        fire.remove([rpos, cpos - 1])

    if matrix[rpos + 1][cpos + 1]['text'] == '@':
        matrix[rpos + 1][cpos + 1]['text'] = ' '
        matrix[rpos + 1][cpos + 1]['bg'] = 'white'
        fire.remove([rpos + 1, cpos + 1])

    if matrix[rpos - 1][cpos + 1]['text'] == '@':
        matrix[rpos - 1][cpos + 1]['text'] = ' '
        matrix[rpos - 1][cpos + 1]['bg'] = 'white'
        fire.remove([rpos - 1, cpos + 1])

    if matrix[rpos + 1][cpos - 1]['text'] == '@':
        matrix[rpos + 1][cpos - 1]['text'] = ' '
        matrix[rpos + 1][cpos - 1]['bg'] = 'white'
        fire.remove([rpos + 1, cpos - 1])

    if matrix[rpos - 1][cpos - 1]['text'] == '@':
        matrix[rpos - 1][cpos - 1]['text'] = ' '
        matrix[rpos - 1][cpos - 1]['bg'] = 'white'
        fire.remove([rpos - 1, cpos - 1])

    lck.release()
    # logging.info('released lock')


def fire_thread_start():
    """Start the burning thread"""
    thread = threading.Thread(target=burn)
    thread.start()


def firemen_thread_start():
    """Start x threads for x firemen"""
    firemen_threads = {}
    for x in range(len(firemen)):
        firemen_threads[x] = threading.Thread(target=move, args=(x,))
        # logging.info(f'Starting thread {firemen_threads[x]} with {firemen[x]}')
        firemen_threads[x].start()


def kill(*args):
    """Killer function"""
    if started:
        startstop()
    root.destroy()


def load_maze(file):
    """Load the maze from the configuration file"""
    logging.info('Loading the maze ...')
    with open(file, 'r', encoding='utf8') as f:
        n = 0
        bl = []
        for line in f:
            if line[0] == '[':
                pass
            elif line.strip() == '':
                break
            else:
                line = line.strip('\n')
                bl.append(line)
                if len(bl[n]) == len(bl[0]):
                    n += 1
                else:
                    logging.critical('All rows must be of the same length. '
                                     'Please edit your configuration file "hasici.ini"')
                    quit(1)
    time.sleep(0.1)
    logging.info('Maze loaded!')
    return bl


def move(x):
    """Complete logic of movement of one fireman"""
    first_run = True
    n = int(x)
    while started:
        fire_flag = False
        direction_dict, closest_fire_dict = count_free_btns(firemen[n])
        if not closest_fire_dict:
            if not first_run:
                free_dirs = 0
                for x in direction_dict.values():
                    if x != 0:
                        free_dirs += 1
                if free_dirs > 1:
                    del direction_dict[last_dir]

            temp_dict = {}
            for x in direction_dict.values():
                temp_dict.setdefault(x, 0)
                temp_dict[x] += 1

            if first_run:
                first_run = False
                if len(temp_dict) == 4:
                    max_dir = max(direction_dict, key=direction_dict.get)
                    max_value = max(direction_dict.values())
                    last_dir = opposite_dir(max_dir)

                else:
                    max_value = sorted(temp_dict)[-1]
                    max_dirs_temp = list({y for y in direction_dict if direction_dict[y] == max_value})
                    max_dir = random.choice(max_dirs_temp)
                    last_dir = opposite_dir(max_dir)

            elif not first_run:
                if len(temp_dict) == 3:
                    max_dir = max(direction_dict, key=direction_dict.get)
                    max_value = max(direction_dict.values())
                    last_dir = opposite_dir(max_dir)

                else:
                    max_value = sorted(temp_dict)[-1]
                    max_dirs_temp = list({y for y in direction_dict if direction_dict[y] == max_value})
                    max_dir = random.choice(max_dirs_temp)
                    last_dir = opposite_dir(max_dir)

            move_a_fireman(max_value, max_dir, firemen[n], n, fire_flag)

        elif closest_fire_dict:
            first_run = False
            fire_flag = True
            if len(closest_fire_dict) == 1:
                fire_dir = list(closest_fire_dict.keys())[0]
                fire_pos = closest_fire_dict[fire_dir]
                fire_value = check_fire_distance(fire_dir, fire_pos, firemen[n])

            elif len(closest_fire_dict) == 2:
                fire_dir1 = list(closest_fire_dict.keys())[0]
                fire_dir2 = list(closest_fire_dict.keys())[1]
                fire_pos1 = closest_fire_dict[fire_dir1]
                fire_pos2 = closest_fire_dict[fire_dir2]
                fire_value1 = check_fire_distance(fire_dir1, fire_pos1, firemen[n])
                fire_value2 = check_fire_distance(fire_dir2, fire_pos2, firemen[n])
                fire_value = min([fire_value1, fire_value2])
                if fire_value == fire_value1 == fire_value2:
                    fire_dir = random.choice([fire_dir1, fire_dir2])
                else:
                    if fire_value1 == fire_value:
                        fire_dir = fire_dir1
                    elif fire_value2 == fire_value:
                        fire_dir = fire_dir2

            elif len(closest_fire_dict) == 3:
                fire_dir1 = list(closest_fire_dict.keys())[0]
                fire_dir2 = list(closest_fire_dict.keys())[1]
                fire_dir3 = list(closest_fire_dict.keys())[2]
                fire_pos1 = closest_fire_dict[fire_dir1]
                fire_pos2 = closest_fire_dict[fire_dir2]
                fire_pos3 = closest_fire_dict[fire_dir3]
                fire_value1 = check_fire_distance(fire_dir1, fire_pos1, firemen[n])
                fire_value2 = check_fire_distance(fire_dir2, fire_pos2, firemen[n])
                fire_value3 = check_fire_distance(fire_dir3, fire_pos3, firemen[n])
                fire_value = min([fire_value1, fire_value2, fire_value3])
                if fire_value == fire_value1 == fire_value2 == fire_value3:
                    fire_dir = random.choice([fire_dir1, fire_dir2, fire_dir3])
                else:
                    if fire_value1 == fire_value:
                        fire_dir = fire_dir1
                    elif fire_value2 == fire_value:
                        fire_dir = fire_dir2
                    elif fire_value3 == fire_value:
                        fire_dir = fire_dir3

            elif len(closest_fire_dict) == 4:
                fire_dir1 = list(closest_fire_dict.keys())[0]
                fire_dir2 = list(closest_fire_dict.keys())[1]
                fire_dir3 = list(closest_fire_dict.keys())[2]
                fire_dir4 = list(closest_fire_dict.keys())[3]
                fire_pos1 = closest_fire_dict[fire_dir1]
                fire_pos2 = closest_fire_dict[fire_dir2]
                fire_pos3 = closest_fire_dict[fire_dir3]
                fire_pos4 = closest_fire_dict[fire_dir4]
                fire_value1 = check_fire_distance(fire_dir1, fire_pos1, firemen[n])
                fire_value2 = check_fire_distance(fire_dir2, fire_pos2, firemen[n])
                fire_value3 = check_fire_distance(fire_dir3, fire_pos3, firemen[n])
                fire_value4 = check_fire_distance(fire_dir4, fire_pos4, firemen[n])
                fire_value = min([fire_value1, fire_value2, fire_value3, fire_value4])
                if fire_value == fire_value1 == fire_value2 == fire_value3 == fire_value4:
                    fire_dir = random.choice([fire_dir1, fire_dir2, fire_dir3, fire_dir4])
                else:
                    if fire_value1 == fire_value:
                        fire_dir = fire_dir1
                    elif fire_value2 == fire_value:
                        fire_dir = fire_dir2
                    elif fire_value3 == fire_value:
                        fire_dir = fire_dir3
                    elif fire_value4 == fire_value:
                        fire_dir = fire_dir4

            last_dir = opposite_dir(fire_dir)
            move_a_fireman(fire_value, fire_dir, firemen[n], n, fire_flag)


def move_a_fireman(value, direction, pos, fm_number, fire_flag, lck=lock):
    """Moving one fireman according to parameters"""
    position = pos[:]
    if fire_flag:
        moves = value
    elif not fire_flag:
        moves = random.randint(1, value)
    for x in range(moves):
        # logging.debug(behind_firemen)
        if len(behind_firemen[fm_number]) > 2:
            del behind_firemen[fm_number][0]
        if not started:
            break
        time.sleep(firemen_speed)
        if not started:
            break
        if direction == 'n':
            firemen[fm_number][0] = position[0] - 1 - x
            if matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] == 'blue':
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] = fm_number + 1

            elif matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] == fire_color:
                lck.acquire()
                fire.remove([firemen[fm_number][0], firemen[fm_number][1]])
                lck.release()
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['state'] = DISABLED
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] = fm_number + 1
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] = 'blue'

                matrix[firemen[fm_number][0] + 1][firemen[fm_number][1]]['text'] = ' '
                matrix[firemen[fm_number][0] + 1][firemen[fm_number][1]]['bg'] = background_color
                matrix[firemen[fm_number][0] + 1][firemen[fm_number][1]]['state'] = ACTIVE
                behind_firemen[fm_number].append([firemen[fm_number][0] + 1, firemen[fm_number][1]])

            elif matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] != '#':
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['state'] = DISABLED
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] = fm_number + 1
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] = 'blue'

                matrix[firemen[fm_number][0] + 1][firemen[fm_number][1]]['text'] = ' '
                matrix[firemen[fm_number][0] + 1][firemen[fm_number][1]]['bg'] = background_color
                matrix[firemen[fm_number][0] + 1][firemen[fm_number][1]]['state'] = ACTIVE
                behind_firemen[fm_number].append([firemen[fm_number][0] + 1, firemen[fm_number][1]])

        elif direction == 's':
            firemen[fm_number][0] = position[0] + 1 + x
            if matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] == 'blue':
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] = fm_number + 1

            elif matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] == fire_color:
                lck.acquire()
                fire.remove([firemen[fm_number][0], firemen[fm_number][1]])
                lck.release()
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['state'] = DISABLED
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] = fm_number + 1
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] = 'blue'

                matrix[firemen[fm_number][0] - 1][firemen[fm_number][1]]['text'] = ' '
                matrix[firemen[fm_number][0] - 1][firemen[fm_number][1]]['bg'] = background_color
                matrix[firemen[fm_number][0] - 1][firemen[fm_number][1]]['state'] = ACTIVE
                behind_firemen[fm_number].append([firemen[fm_number][0] - 1, firemen[fm_number][1]])

            elif matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] != '#':
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['state'] = DISABLED
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] = fm_number + 1
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] = 'blue'

                matrix[firemen[fm_number][0] - 1][firemen[fm_number][1]]['text'] = ' '
                matrix[firemen[fm_number][0] - 1][firemen[fm_number][1]]['bg'] = background_color
                matrix[firemen[fm_number][0] - 1][firemen[fm_number][1]]['state'] = ACTIVE
                behind_firemen[fm_number].append([firemen[fm_number][0] - 1, firemen[fm_number][1]])

        elif direction == 'w':
            firemen[fm_number][1] = position[1] - 1 - x
            if matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] == 'blue':
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] = fm_number + 1

            elif matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] == fire_color:
                lck.acquire()
                fire.remove([firemen[fm_number][0], firemen[fm_number][1]])
                lck.release()
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['state'] = DISABLED
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] = fm_number + 1
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] = 'blue'

                matrix[firemen[fm_number][0]][firemen[fm_number][1] + 1]['text'] = ' '
                matrix[firemen[fm_number][0]][firemen[fm_number][1] + 1]['bg'] = background_color
                matrix[firemen[fm_number][0]][firemen[fm_number][1] + 1]['state'] = ACTIVE
                behind_firemen[fm_number].append([firemen[fm_number][0], firemen[fm_number][1] + 1])

            elif matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] != '#':
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['state'] = DISABLED
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] = fm_number + 1
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] = 'blue'

                matrix[firemen[fm_number][0]][firemen[fm_number][1] + 1]['text'] = ' '
                matrix[firemen[fm_number][0]][firemen[fm_number][1] + 1]['bg'] = background_color
                matrix[firemen[fm_number][0]][firemen[fm_number][1] + 1]['state'] = ACTIVE
                behind_firemen[fm_number].append([firemen[fm_number][0], firemen[fm_number][1] + 1])

        elif direction == 'e':
            firemen[fm_number][1] = position[1] + 1 + x
            if matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] == 'blue':
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] = fm_number + 1

            elif matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] == fire_color:
                lck.acquire()
                fire.remove([firemen[fm_number][0], firemen[fm_number][1]])
                lck.release()
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['state'] = DISABLED
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] = fm_number + 1
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] = 'blue'

                matrix[firemen[fm_number][0]][firemen[fm_number][1] - 1]['text'] = ' '
                matrix[firemen[fm_number][0]][firemen[fm_number][1] - 1]['bg'] = background_color
                matrix[firemen[fm_number][0]][firemen[fm_number][1] - 1]['state'] = ACTIVE
                behind_firemen[fm_number].append([firemen[fm_number][0], firemen[fm_number][1] - 1])

            elif matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] != '#':
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['state'] = DISABLED
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['text'] = fm_number + 1
                matrix[firemen[fm_number][0]][firemen[fm_number][1]]['bg'] = 'blue'

                matrix[firemen[fm_number][0]][firemen[fm_number][1] - 1]['text'] = ' '
                matrix[firemen[fm_number][0]][firemen[fm_number][1] - 1]['bg'] = background_color
                matrix[firemen[fm_number][0]][firemen[fm_number][1] - 1]['state'] = ACTIVE
                behind_firemen[fm_number].append([firemen[fm_number][0], firemen[fm_number][1] - 1])


def opposite_dir(d):
    """Get the opposite direction"""
    if d == 'n':
        return 's'
    elif d == 's':
        return 'n'
    elif d == 'w':
        return 'e'
    elif d == 'e':
        return 'w'


def startstop():
    """Start and stop"""
    global started

    if not started:
        started = True
        startbutton['text'] = 'STOP'
        startbutton['bg'] = 'red'
        startlabel['text'] = ' '
        fire_thread_start()
        firemen_thread_start()

    elif started:
        started = False
        startbutton['text'] = 'START'
        startbutton['bg'] = 'green'
        startlabel['text'] = 'Klikni...'


maze = load_maze('hasici.ini')
root = Tk()
root.title('Hasici')
root.configure(bg=background_color)
root.option_add('*Font', 'Verdana 14')
root.focus()

root.bind('<Escape>', kill)
root.protocol('WM_DELETE_WINDOW', kill)

matrix = []
fire = []
firemen = []
mrow = 0
mcolumn = 0

for i in maze:
    matrix.append([])
    root.rowconfigure(mrow, weight=1)
    for j in i:
        root.columnconfigure(mcolumn, weight=1)
        if j == '#':
            bgcolor = 'black'
        elif j == '@':
            bgcolor = fire_color
            fire.append([mrow, mcolumn])
        elif j == 'H':
            bgcolor = 'blue'
            firemen.append([mrow, mcolumn])
            j = len(firemen)
        else:
            bgcolor = background_color
        b = Button(root, text=j, bg=bgcolor, command=lambda x=mrow, y=mcolumn: extinguish(x, y))
        b.grid(row=mrow, column=mcolumn, sticky='NSEW')
        if j == '#':
            b['state'] = DISABLED
        elif bgcolor == 'blue':
            b['state'] = DISABLED
        matrix[mrow].append(b)
        mcolumn += 1
    mrow += 1
    mcolumn = 0

behind_firemen = {}
for y in range(len(firemen)):
    behind_firemen[y] = []

n_rows = len(matrix)
n_columns = len(matrix[0])

startlabel = Label(root, text='Klikni...', bg=background_color)
startbutton = Button(root, text='START', bg='green', command=startstop)
startlabel.grid(row=n_rows + 1, columnspan=n_columns)
startbutton.grid(row=n_rows + 2, columnspan=n_columns)

root.mainloop()
