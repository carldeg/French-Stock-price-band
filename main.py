from tkinter import *
import tkinter as tk
from DataBaseManagement import SQL_Manager as dbm
from db_feed import *


class App(Tk):

    def __init__(self):

        Tk.__init__(self)
        geo = '{0}x{1}+{2}+{3}'.format(3000, 50, 0, 0)
        self.geometry(geo)
        self.overrideredirect(1)
        self.attributes("-alpha", 0.85)

        #self.wm_attributes("-topmost", "true")

        self.maincv = tk.Canvas(self, background='black', border=0, highlightthickness=0,state=DISABLED)
        self.maincv.pack(fill='both', expand=True)
        self.count = 0
        self.dx = -5
        self.dy = 0

        self.d = dbm('Prices').get_table_as_df('LivePrice')
        InsertMobile().fill_db('LivePrice')
        self.box()
        self.deplacement()

    def box(self):

        self.d = dbm('Prices').get_table_as_df('LivePrice')

        self.res = {

        }

        x = 1920
        for i in range(len(self.d)):

            self.bigbox = tk.Canvas(self.maincv, background='black', border=0, highlightthickness=0, height=50,
                                    width=200)

            self.namebox = tk.Canvas(self.bigbox, background='black', border=0, highlightthickness=0)
            self.namebox.place(x=5, y=5, height=40, width=120)

            self.varbox = tk.Canvas(self.bigbox, background='black', border=0, highlightthickness=0)
            self.varbox.place(x=135, y=5, height=40, width=60)

            self.pricebox = tk.Canvas(self.bigbox, background='black', border=0, highlightthickness=0)
            self.pricebox.place(x=205, y=5, height=40, width=60)

            if float(self.d.iloc[i, 4]) > 0:
                fontcolor = 'green'

            elif float(self.d.iloc[i, 4]) < 0:
                fontcolor = 'red'

            tk.Label(self.varbox, text=str(self.d.iloc[i, 4]) + ' %', font='Arial 9 bold', background='black',
                     foreground=fontcolor).place(x=5, y=10,
                                                 width=50,
                                                 height=20)
            tk.Label(self.pricebox, text=self.d.iloc[i, 3], font='Arial 9 bold', background='black',
                     foreground=fontcolor).place(x=0, y=10,
                                                 width=50,
                                                 height=20)
            tk.Label(self.namebox, text=self.d.iloc[i, 1], font='Arial 9 bold', background='black', foreground='white',
                     justify=RIGHT, anchor='e').place(x=5, y=10,
                                                      width=110,
                                                      height=20)
            self.res[self.d.iloc[i, 1]] = self.maincv.create_window((x, 25), height=50, width=300,
                                                                    window=self.bigbox)

            x += 300

        return self.bigbox

    def deplacement(self):
        if self.count <= -(303 * len(self.d)):  # x*len(self.d)
            self.maincv.pack_forget()
            self.__init__()
            return

        else:
            self.count += self.dx
            for i in self.res.keys():
                self.maincv.move(self.res[i], self.dx, self.dy)

        self.after(175, self.deplacement)  # 175


App().mainloop()
