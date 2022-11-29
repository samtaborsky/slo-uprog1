import tkinter.messagebox
from sqlite3 import dbapi2 as sqlite
from tkinter import *
import os
import random
import threading
import time


db_open = False
interval = 1
ovoce_dict = []
rozsah = 15


def zmenit(*args):
    global rozsah, interval, ovoce_dict
    try:
        rozsah = int(rozsah_entry.get())
        interval = float(int_entry.get())
    except ValueError:
        tkinter.messagebox.showerror('Chyba', 'Spatne udaje!')
        int_entry.delete(0, END)
        rozsah_entry.delete(0, END)
    finally:
        ovoce_dict[-1]['text'] = f'{interval}s  ... +- 1-{rozsah}ks'


def pocet_rows():
    cursor.execute('SELECT COUNT(id) FROM ovoce')
    pocet = cursor.fetchone()[0]
    if pocet is None:
        return 0
    else:
        return pocet


def vykresli():
    global ovoce_dict
    rows = cursor.execute('SELECT * FROM ovoce').fetchall()
    n = 1
    for x in range(pocet_rows()):
        lab = Label(root, text=f'{rows[x][1]}  ...  {rows[x][2]}ks')
        lab.grid(row=n, columnspan=5, sticky='EW')
        ovoce_dict.append(lab)
        n += 1
    intlab = Label(root, text=f'{interval}s  ... +- 1-{rozsah}ks')
    intlab.grid(row=n, columnspan=5, sticky='EW')
    ovoce_dict.append(intlab)


def run_thread():
    global db_open
    db_open = True
    thread = threading.Thread(target=aktualizuj)
    thread.start()


def aktualizuj():
    global db_open

    while db_open:
        global ovoce_dict
        rows = cursor.execute('SELECT * FROM ovoce').fetchall()
        for row in rows:
            new_pocetks = random.randint(-rozsah, rozsah)
            db.execute('UPDATE ovoce SET kusu = kusu + ? WHERE id == ?', (new_pocetks, row[0]))
            db.commit()
            cursor.execute('SELECT * FROM ovoce WHERE id == ?', [row[0]])
            c = cursor.fetchall()
            if c[0][2] <= 0:
                ovoce_dict[row[0]-1].destroy()
                cursor.execute('DELETE FROM ovoce WHERE id == ?', [row[0]])
                db.commit()
            else:
                ovoce_dict[row[0]-1]['text'] = f'{c[0][1]}  ...  {c[0][2]}ks'
        if pocet_rows() == 0:
            tkinter.messagebox.showinfo('Info', 'Sklad je prazdny!')
            break
        else:
            time.sleep(interval)

    db.close()


def kill(*args):
    global db_open
    db_open = False
    db.close()
    root.destroy()


zbozi = ['jablka', 'hrusky', 'hrozno', 'grapefruit', 'kiwi']
pocetkusu = [(z, random.randint(10, 100)) for z in zbozi]

db = sqlite.connect('l08_u3.sqlite', check_same_thread=False)
cursor = db.cursor()
db.execute('DROP TABLE ovoce')
db.execute('CREATE TABLE ovoce(id INTEGER PRIMARY KEY AUTOINCREMENT, nazev TEXT, kusu INTEGER)')
db.executemany('INSERT INTO ovoce(nazev, kusu) VALUES(?, ?)', pocetkusu)

root = Tk()
path = os.path.dirname(__file__) + r'\grape.ico'
root.iconbitmap(path)
root.option_add('*Font', 'Verdana 12')
root.title('Ovoce')
root.focus()
root.bind('<Escape>', kill)
root.bind('<Return>', zmenit)
root.protocol('WM_DELETE_WINDOW', kill)

int_label = Label(root, text='Interval [s]')
int_entry = Entry(root)
int_entry.insert(0, str(interval))
rozsah_label = Label(root, text='Rozsah [ks]')
rozsah_entry = Entry(root)
rozsah_entry.insert(0, str(rozsah))
zmena_bt = Button(root, text='Zmenit', command=zmenit)

int_label.grid(row=0, column=1, sticky='E')
int_entry.grid(row=0, column=2, sticky='EW')
rozsah_label.grid(row=0, column=3, sticky='E')
rozsah_entry.grid(row=0, column=4, sticky='EW')
zmena_bt.grid(row=0, column=5, sticky='EW')

vykresli()
for i in range(root.grid_size()[0]):
    root.columnconfigure(i, weight=1)
for j in range(root.grid_size()[1]):
    root.rowconfigure(j, weight=1)

run_thread()
root.mainloop()
