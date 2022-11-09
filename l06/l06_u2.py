from tkinter import *
from random import choice
from time import time

started = False
clicked = False
moznosti = ['A', 'B', 'C', 'D']
starttime = 0
stoptime = 0
n = 0
total = 0
avgtime_total = 0
pocetspravnych_n = 0


def gen():
    global clicked, starttime
    if started:
        if clicked:
            textlabel['text'] = choice(moznosti)
            clicked = False
            starttime = time()
        else:
            pass
    root.after(1, gen)


def start():
    global started, starttime
    started = True
    startbt['text'] = 'STOP'
    textlabel['text'] = choice(moznosti)
    starttime = time()


def stop():
    global started
    started = False
    startbt['text'] = 'START'
    textlabel['text'] = '----'


def startclick():
    if started:
        stop()
    else:
        start()


def choiceclick(bt):
    global clicked, stoptime, total, n, avgtime_total, pocetspravnych_n
    if started:
        stoptime = time()
        time1 = round(stoptime-starttime, 3)
        total += time1
        n += 1
        avgtime_total = total/n
        timelabel['text'] = 'Time: ' + str(time1)
        if bt == textlabel['text']:
            pocetspravnych_n += 1
            avgtime['text'] = 'Avg. time: ' + str(round(avgtime_total, 3))
            pocetspravnych['text'] = 'Spravne: ' + str(pocetspravnych_n)
        else:
            avgtime_total += 1
            avgtime['text'] = 'Avg. time: ' + str(round(avgtime_total, 3))
        clicked = True


root = Tk()
root.title('Hra')
root.option_add('*Font', 'Verdana 16')

startbt = Button(root, text='START', font='Verdana 10', command=startclick)
timelabel = Label(root, text='Time: ----', font='Verdana 10')
textlabel = Label(root, text='----')
avgtime = Label(root, text='Avg. time: ----', font='Verdana 10')
pocetspravnych = Label(root, text='Spravne: ', font='Verdana 10')
blank = Label(root, text='               ')
bt1 = Button(root, text='A', command=lambda btn='A': choiceclick(btn))
bt2 = Button(root, text='B', command=lambda btn='B': choiceclick(btn))
bt3 = Button(root, text='C', command=lambda btn='C': choiceclick(btn))
bt4 = Button(root, text='D', command=lambda btn='D': choiceclick(btn))

startbt.grid(row=0, column=0, sticky=W)
timelabel.grid(row=4, column=0, sticky=W)
textlabel.grid(row=0, column=1, columnspan=2, rowspan=2)
avgtime.grid(row=5, column=0, sticky=W)
pocetspravnych.grid(row=6, column=0, sticky=W)
blank.grid(row=0, column=3, columnspan=1)

bt1.grid(row=2, column=1, sticky='ENWS')
bt2.grid(row=2, column=2, sticky='ENWS')
bt3.grid(row=3, column=1, sticky='ENWS')
bt4.grid(row=3, column=2, sticky='ENWS')

rows = root.grid_size()[0]
columns = root.grid_size()[1]

for i in range(rows):
    root.rowconfigure(i, weight=1)

for i in range(columns):
    root.columnconfigure(i, weight=1)

root.after(1, gen)
root.mainloop()
