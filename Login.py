# imports
from tkinter import *
from tkinter import messagebox as ms
import sqlite3
import tkinter
# make database and users (if not exists already) table at programme start up
with sqlite3.connect('quit.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL ,password TEX NOT NULL);')
db.commit()
db.close()


# main Class
class main:
    def __init__(self, master):
        # Window
        self.master = master
        # Some Usefull variables
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        # Create Widgets
        self.widgets()

    # Login Function
    def login(self):
        # Establish Connection
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()

        # Find user If there is any take proper action
        find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
        c.execute(find_user, [(self.username.get()), (self.password.get())])
        result = c.fetchall()
        if result:
            msg = ""
            self.logf.pack_forget()
            self.head['text'] = self.username.get() + '\n Loged In'
            msg = self.head['text']
            #            self.head['pady'] = 150
            print(msg)
            # ===========================================
            root.destroy()


            from subprocess import call
            call(["python", "Home.py"])

            # ================================================
        else:
            ms.showerror('Oops!', 'Username Not Found.')

    def new_user(self):
        # Establish Connection
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()

        # Find Existing username if any take proper action
        find_user = ('SELECT * FROM user WHERE username = ?')
        c.execute(find_user, [(self.username.get())])
        if c.fetchall():
            ms.showerror('Error!', 'Username Taken Try a Diffrent One.')
        else:
            ms.showinfo('Success!', 'Account Created Successfully !')
            self.log()
        # Create New Account
        insert = 'INSERT INTO user(username,password) VALUES(?,?)'
        c.execute(insert, [(self.n_username.get()), (self.n_password.get())])
        db.commit()

        # Frame Packing Methords

    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()

    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()



    # Draw Widgets
    def widgets(self):
        self.head = Label(self.master, text='Welcome',background="white", font=('Times New Roman', 35), pady=20)
        self.head.pack()

        self.head.pack()
        self.head = Label(self.master, text='LOGIN',background="white", font=('Times New Roman', 35), pady=10)
        self.head.pack()
        self.logf = Frame(self.master, padx=6, pady=6,background="white")
        Label(self.logf, text='Username: ',background="snow",font=("Tempus Sans ITC", 30), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.username, bd=5,background="white", font=('', 15)).grid(row=0, column=1)
        Label(self.logf, text='Password: ',background="snow",font=("Tempus Sans ITC", 30), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        Button(self.logf, text=' Login ', bd=3,font=("Tempus Sans ITC", 20),background="black",foreground="white", padx=5, pady=5, command=self.login).grid()
        Button(self.logf, text=' Create Account ',font=("Tempus Sans ITC", 20),background="black",foreground="white", bd=3,padx=5, pady=5, command=self.cr).grid(row=2,
                                                                                                              column=1)


        self.logf.pack()

        self.crf = Frame(self.master, padx=10, pady=10)

        Label(self.crf, text='Username: ', font=("Tempus Sans ITC", 20),background="black",foreground="white", pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.n_username, bd=5, font=('', 15)).grid(row=0, column=1)
        Label(self.crf, text='Password: ', font=("Tempus Sans ITC", 20),background="black",foreground="white", pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.n_password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        Button(self.crf, text='Create Account', bd=3,font=("Tempus Sans ITC", 20),background="black",foreground="white", padx=5, pady=5, command=self.new_user).grid()
        Button(self.crf, text='Go to Login', bd=3,font=("Tempus Sans ITC", 20),background="black",foreground="white", padx=5, pady=5, command=self.log).grid(row=2,
                                                                                                         column=1)

from tkinter import *
from PIL import ImageTk, Image
import os

root = Tk()

root.configure(background="white")
root.geometry("1200x650")
root.title("Login Form")
main(root)

root.mainloop()


