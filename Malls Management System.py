import sqlite3
from tkinter import *

counter=0
t2=0
t1=0
t3values=0
t4=0
t5=0
t6=0
class MallsTable:

    def __init__(self):
        self.conn = sqlite3.connect("dbs\project3DB.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS malls (ID INTEGER NOT NULL,name TEXT NOT NULL,type TEXT NOT NULL,address TEXT NOT NULL,coordinates TEXT NOT NULL,manager_name TEXT NOT NULL)")

    def display(self):
        self.cur.execute("SELECT * FROM malls")
        self.records= self.cur.fetchall()
        print(self.records)
        return self.records
    
    def search(self,name):
        self.cur.execute("SELECT * FROM malls WHERE name = ?",(name,))
        self.records= self.cur.fetchone()
        print(self.records)
        return self.records

    def insert(self, ID,name,type,address,coordinates,manager_name):
        if (ID=="" or name=="" or type=="" or address=="" or coordinates=="" or manager_name==""):
            raise Exception("One of the entry fields is empty")
        self.cur.execute("INSERT INTO malls VALUES (?,?,?,?,?,?)", (ID,name,type,address,coordinates,manager_name))
        self.conn.commit()
        self.clearEntries(t1,t2,t4,t5,t6)

    def update(self,valueToUpdate,ID):
        global t1,t2,t3values,t4,t5,t6
        if (ID==""):
            raise Exception("You have to select an ID to update its values")
        if valueToUpdate=="Name":
            valuesToUpdate=t2.get()
            columnToUpdate="name"
            print(valuesToUpdate,valueToUpdate,columnToUpdate)
        elif valueToUpdate=="Type":
            valuesToUpdate=t3values.get()
            columnToUpdate="type"
        elif valueToUpdate=="Address":
            valuesToUpdate=t4.get()
            columnToUpdate="address"
        elif valueToUpdate=="Coordinates":
            valuesToUpdate=t5.get()
            columnToUpdate="coordinates"
        elif valueToUpdate=="Manager Name":
            valuesToUpdate=t6.get()
            columnToUpdate="manager_name"
        self.cur.execute(f"UPDATE malls SET {columnToUpdate} = ? WHERE ID = ?", (valuesToUpdate,ID))
        self.conn.commit()
        self.clearEntries(t1,t2,t4,t5,t6)

    def delete(self,ID):
        if (ID==""):
            raise Exception("You have to select an ID to delete its corresponding values")
        self.cur.execute("DELETE FROM malls WHERE ID = ?",(ID))
        self.conn.commit()
        self.clearEntries(t1,t2,t4,t5,t6)
    
    def clearEntries(self,t1,t2,t4,t5,t6):
        t1.delete(0,END)
        t2.delete(0,END)
        t4.delete(0,END)
        t5.delete(0,END)
        t6.delete(0,END)

    def __del__(self):
        self.conn.close()
    
    def openOrClose(self,btn):
        global counter
        if counter==0:
            self.__del__()
            counter=1
            btn.config(text=f"\tOpen Database\t")
        elif counter==1:
            self.__init__()
            counter=0
            btn.config(text=f"\tClose Database\t")
    
    
def display(lb1,list):
    if list==[]:
        lb1.delete(0,END)
        Msg="Error 404: there are no malls entered yet."
        lb1.insert(0,Msg)
    else:
        lb1.delete(0,END)
        for i in list:
            lb1.insert(END,i)

def search(lb1,mosque):
    global t2
    if t2.get()=='':
        lb1.delete(0,END)
        Msg="Input Error: there are no inputs supplied."
        lb1.insert(0,Msg)
    elif mosque==None:
        lb1.delete(0,END)
        Msg="Error 404: there are no malls with that name."
        lb1.insert(0,Msg)
    else:
        lb1.delete(0,END)
        lb1.insert(END,mosque)

mainWindow = Tk()
mainWindow.title('Malls Management System')
mainWindow.geometry('1000x200')

l1 = Label(mainWindow, text=f"  ID  ", font="Default")
l1.grid(row=0,column=0,rowspan=2)
t1 = Entry(mainWindow)
t1.grid(row=0,column=2,rowspan=2)

l2 = Label(mainWindow, text=f"  Name  ", font="Default")
l2.grid(row=0,column=3,rowspan=2)
t2 = Entry(mainWindow)
t2.grid(row=0,column=4,rowspan=2)
########
l3 = Label(mainWindow, text=f"  Type  ", font="Default")
l3.grid(row=2,column=0,rowspan=2)
options = ["Outdoor","Indoor"]
t3values = StringVar(mainWindow)
t3 = OptionMenu(mainWindow, t3values, *options)
t3.grid(row=2,column=2,rowspan=2)

l4 = Label(mainWindow, text=f"  Address  ", font="Default")
l4.grid(row=2,column=3,rowspan=2)
t4 = Entry(mainWindow)
t4.grid(row=2,column=4,rowspan=2)
#######
l5 = Label(mainWindow, text=f"  Coordinates  ", font="Default")
l5.grid(row=4,column=0,rowspan=2)
t5 = Entry(mainWindow)
t5.grid(row=4,column=2,rowspan=2)

l7 = Label(mainWindow, text=f"  To Update  ", font="Default")
l7.grid(row=6,column=0,rowspan=2)
optionsToUpdate = ["Name","Type","Address","Coordinates","Manager Name"]
valuesToUpdate = StringVar(mainWindow)
t7 = OptionMenu(mainWindow, valuesToUpdate, *optionsToUpdate)
t7.grid(row=6,column=2,rowspan=2)

l6 = Label(mainWindow, text=f"  Manager Name  ", font="Default")
l6.grid(row=4,column=3,rowspan=2)
t6 = Entry(mainWindow)
t6.grid(row=4,column=4,rowspan=2)

b1 = Button(mainWindow, text=f"\tDisplay All\t")
b1.grid(row=8,column=2,rowspan=2)
b2 = Button(mainWindow, text=f"\tSearch by Name\t")
b2.grid(row=8,column=3,rowspan=2)
b3 = Button(mainWindow, text=f"\tUpdate by ID\t")
b3.grid(row=8,column=4,rowspan=2)
b4 = Button(mainWindow, text=f"\tAdd Entry\t")
b4.grid(row=10,column=2,rowspan=2)
b5 = Button(mainWindow, text=f"\tDelete by ID\t")
b5.grid(row=10,column=3,rowspan=2)
b6 = Button(mainWindow, text=f"\tClose Database\t")
b6.grid(row=10,column=4,rowspan=2)

lb1 = Listbox(mainWindow,width=65,height=10)
lb1.grid(row=0,column=5,rowspan=10,columnspan=1)
newObj = MallsTable()

# Click Event
b1.bind('<Button-1>',lambda e: display(lb1,newObj.display()))
b2.bind('<Button-1>',lambda e: search(lb1,(newObj.search(t2.get()))))
b3.bind('<Button-1>',lambda e: newObj.update(valuesToUpdate.get(),t1.get()))
b4.bind('<Button-1>',lambda e: newObj.insert(t1.get(),t2.get(),t3values.get(),t4.get(),t5.get(),t6.get()))
b5.bind('<Button-1>',lambda e: newObj.delete(t1.get()))
b6.bind('<Button-1>',lambda e: newObj.openOrClose(b6))


# Hover Event
def hover(widget):
    widget.config(cursor="tcross",bg="#aaaaaa")

def notHover(widget):
    widget.config(cursor="arrow",bg="#f0f0f0")


# Hover Event
b1.bind('<Enter>',lambda e: hover(b1))
b2.bind('<Enter>',lambda e: hover(b2))
b3.bind('<Enter>',lambda e: hover(b3))
b4.bind('<Enter>',lambda e: hover(b4))
b5.bind('<Enter>',lambda e: hover(b5))
b6.bind('<Enter>',lambda e: hover(b6))
t3.bind('<Enter>',lambda e: hover(t3))
t7.bind('<Enter>',lambda e: hover(t7))
b1.bind('<Leave>',lambda e: notHover(b1))
b2.bind('<Leave>',lambda e: notHover(b2))
b3.bind('<Leave>',lambda e: notHover(b3))
b4.bind('<Leave>',lambda e: notHover(b4))
b5.bind('<Leave>',lambda e: notHover(b5))
b6.bind('<Leave>',lambda e: notHover(b6))
t3.bind('<Leave>',lambda e: notHover(t3))
t7.bind('<Leave>',lambda e: notHover(t7))



mainWindow.mainloop()