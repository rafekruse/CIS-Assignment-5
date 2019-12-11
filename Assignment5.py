from tkinter import *
import tkinter as tk
import sqlite3 as sql
import sys

com = sql.connect('flowers2019.db')
db = com.cursor()

def pcmd(output):
    sys.stdout.write(str(output) + str("\n"))  # same as print
    sys.stdout.flush()


window = tk.Tk()
window.geometry("1000x700")

background_image=tk.PhotoImage(file = 'bg.png')
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


db.execute("SELECT DISTINCT NAME FROM SIGHTINGS")
result = db.fetchall()

flower_frame = Frame(window)
flower_frame.pack(side="left")

listNodes = Listbox(flower_frame, width=30, height=30, font=("Helvetica", 15), fg = "black", selectbackground = "green")
listNodes.configure(background = '#35ab68')
listNodes.pack(side="left", fill="y")

scrollbar = Scrollbar(flower_frame, orient="vertical")
scrollbar.config(command=listNodes.yview)
scrollbar.pack(side="right", fill="y")

listNodes.config(yscrollcommand=scrollbar.set)

for i in range(0, len(result)):
    listNodes.insert(END, str(result[i][0]))




db_frame = Frame(window)
db_frame.place(x = 675, y = 50, anchor = 'n')

db_label_text = tk.StringVar(window)
db_label_text.set("Select a flower.")
db_label = Label(window, textvariable = db_label_text, font=("Helvetica", 21, 'bold'), borderwidth=2, relief="solid", foreground = "white")
db_label.configure(background = '#0c7827')
db_label.place(x = 675, y = 5, anchor = 'n')


def save(event, flower, row, col):

    col_name = "person"
    if col == 1:
        col_name = "location"
    if col == 2:
        col_name = "sighted"

    new_value = table[row][col].get("1.0",END).rstrip()

    if new_value == "" and col == 0:
        cmd = "Delete from SIGHTINGS Where name = (SELECT Name FROM SIGHTINGS WHERE Name= \"" + flower + "\" ORDER BY Sighted Limit 1 OFFSET " + str(row - 1) +  ") And sighted = (SELECT sighted FROM SIGHTINGS WHERE Name=  \"" + flower + "\"  ORDER BY Sighted Limit 1 OFFSET " + str(row - 1) +  ");"
    else:
        cmd = "Update SIGHTINGS Set " + col_name + " = \"" + new_value  + "\" Where name = (SELECT Name FROM SIGHTINGS WHERE Name= \"" + flower + "\" ORDER BY Sighted Limit 1 OFFSET " + str(row - 1) +  ") And sighted = (SELECT sighted FROM SIGHTINGS WHERE Name=  \"" + flower + "\"  ORDER BY Sighted Limit 1 OFFSET " + str(row - 1) +  ");"
    pcmd(cmd)
    db.execute(cmd)
    com.commit()


person = Label(db_frame, text = "Person", wraplength=150, font=("Helvetica", 13), borderwidth=1, relief="solid", foreground = "white")
person.configure(background = '#0c7827')
person.config(height = 2, width = 18)
person.grid(row = 0, column = 0)
location = Label(db_frame, text = "Location", wraplength=150, font=("Helvetica", 13), borderwidth=1, relief="solid", foreground = "white")
location.configure(background = '#0c7827')
location.config(height = 2, width = 18)
location.grid(row = 0, column = 1)
date = Label(db_frame, text = "Date Sighted", wraplength=150, font=("Helvetica", 13), borderwidth=1, relief="solid", foreground = "white")
date.configure(background = '#0c7827')
date.config(height = 2, width = 18)
date.grid(row = 0, column = 2)

table = [[None] * 3 for i in range(10)]
pcmd(str(len(table)) + " " + str(len(table[0])))

for i in range (1, min(len(result)+1,11)):
    for j in range(3):
        b = Text(db_frame, wrap = WORD, font=("Helvetica", 13), borderwidth=1, relief="solid")
        if i % 2 == 0:
            b.configure(background = '#9ad9aa')
        else:           
            b.configure(background = '#c1e0c9')
        b.config(height = 2, width = 18)
        b.grid(row = i, column = j)
        table[i - 1][j] = b


insert_b = Button(window, text = "Insert New Entry", font=("Helvetica", 15), borderwidth=3, relief="raised")
insert_b.place(x = 675, y = 585, anchor = 'n') 
insert_b.config(height = 1,width = 15)
insert_b.configure(background = '#9ad9aa')


def insert(current_flower, a, b, c):
    db.execute('INSERT INTO SIGHTINGS VALUES (?,?,?,?)', [current_flower, a, b, c])
    com.commit()
    
    insert_one.delete('1.0', END)
    insert_two.delete('1.0', END)
    insert_three.delete('1.0', END)

    update_table(current_flower)

insert_one = Text(window, wrap = WORD, font=("Helvetica", 13), borderwidth=1, relief="solid")
insert_one.config(height = 2, width = 18)
insert_one.configure(background = '#9ad9aa')
insert_one.place(x = 508, y = 540, anchor = 'n')
    
insert_two = Text(window, wrap = WORD, font=("Helvetica", 13), borderwidth=1, relief="solid")
insert_two.config(height = 2, width = 18)
insert_two.configure(background = '#9ad9aa')
insert_two.place(x = 674, y = 540, anchor = 'n')

insert_three = Text(window, wrap = WORD, font=("Helvetica", 13), borderwidth=1, relief="solid")
insert_three.config(height = 2, width = 18)
insert_three.configure(background = '#9ad9aa')
insert_three.place(x = 840, y = 540, anchor = 'n')








def onselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    
    insert_b.configure(command = lambda : insert(value, insert_one.get("1.0",END), insert_two.get("1.0",END), insert_three.get("1.0",END)))

    update_table(value)

def update_table(value):    
    db_label_text.set(value + " Sightings")



    query = "SELECT Person, Location, Sighted FROM SIGHTINGS WHERE Name='"+value+"' ORDER BY Sighted;"
    db.execute(query)
    result = db.fetchall()



    for i in range (0, 10):
        for j in range(3):
            table[i][j].delete('1.0', END)
            if(len(result) > i):
                table[i][j].insert(tk.END, str(result[i - 1][j]))
                table[i][j].bind("<KeyRelease>", lambda event, flower = value, row = i, col = j: save(event,flower, row, col))

            

    


    



listNodes.bind('<<ListboxSelect>>', onselect)


window.mainloop()