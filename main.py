from tkinter import *
from os import system
from tkinter.messagebox import showinfo, showwarning, showerror
import sqlite3


# ==================settings==================
rootwindow = Tk()
rootwindow.title("Safa Library Manager")
rootwindow.geometry("700x300")


rootwindow.resizable(width=False, height=False)
textcolor = "black"
try:
    file_themcolor = open("themcolor.txt")
    themcolor = file_themcolor.read().split("\n")
    color = themcolor[0]
    textcolor = themcolor[1]
    file_themcolor.close()
    del file_themcolor
except:
    color = "gray"
    File_themcolor = open("themcolor.txt","w")
    File_themcolor.write("gray\nblack")
    File_themcolor.close()
    showwarning("error in themcolor.txt","file themcolor.txt for edit them app, it has an error. themcolor.txt file created."
                                          " them color background set gray.")


try:
    rootwindow.configure(bg=color)
except:
    color = "gray"
    rootwindow.configure(bg="gray")
    file_themcolor = open("themcolor.txt","r")
    showwarning("Color not found!",f"color {file_themcolor.read()} not found. color is set gray")
    file_themcolor.close()
    file_themcolor = open("themcolor.txt","w")
    file_themcolor.write("gray\nblack")
    file_themcolor.close()

name_lib_forinstall = StringVar(rootwindow)
about_lib_selected_forinstall = StringVar(rootwindow)

# ==================Function==================


select_lib = None
select_lib_forinstall = None
def search_lib_state(state):
    if state == "ON":
        btn_install_lib.configure(state="normal")
        lib_name_forinstall.configure(state="normal")
    else:
        btn_install_lib.configure(state="disabled")
        lib_name_forinstall.configure(state="disabled")

def get_selected_lib(event):
    # print(lib_list.curselection())
    if len(lib_list.curselection()) > 0:
        index = lib_list.curselection()[0]
        global select_lib
        select_lib = lib_list.get(index)
        search_lib_state("ON")
        name_lib_forinstall.set("")


def install_lib():
    lib_name = lib_name_forinstall.get()
    if lib_name in lib_list.get(0,END):
        showerror("install library","The library you want is installed.")
        return None
    system(f"pip install {lib_name} > tmp.txt")

    tmp = open("tmp.txt")
    if tmp.read() == "":
        showerror("install library",f"{lib_name} not found.")
        return None
    tmp.close()


    lib_list.insert(0,lib_name)
    value_number_lib_label = StringVar(rootwindow, f"Number Lib: {len(lib_list.get(0, END))}")
    showinfo("installed library",f"The {lib_name} Library was installed")

def load_liblist():
    system("pip list > tmp.txt")

    LIBSfile = open("tmp.txt", "r")

    lib = LIBSfile.read()
    LIBSfile.close()
    lib_split_line = lib.split("\n")
    libs = []

    for item in lib_split_line:
        libs.append(item.split(" ")[0])


    libs.pop(0)
    libs.pop(0)
    libs.pop()
    # libs.remove("")
    lib_list.delete(0, END)
    for lib in libs:
        lib_list.insert(0, lib)
    value_number_lib_label = StringVar(rootwindow, f"Number Lib: {len(lib_list.get(0, END))}")

    search_lib_state("ON")
    name_lib_forinstall.set("")




def delete_lib():
    index = lib_list.curselection()[0]
    lib_list.delete(index)
    system(f"pip uninstall {select_lib} -y")
    load_liblist()
    value_number_lib_label = StringVar(rootwindow, f"Number Lib: {len(lib_list.get(0, END))}")




def about_lib():
    if select_lib == None:
        showwarning("No Select", "Please select the library")
        return None
    system(f"pip show {select_lib} > tmp.txt")
    file_data = open("tmp.txt","r")
    data = file_data.read()
    file_data.close()
    showinfo(f"About {select_lib}",data)

def get_selected_lib_forinstall(event):
    # print(lib_forinstall_list.curselection())'
    if len(lib_forinstall_list.curselection()) > 0:
        index2 = lib_forinstall_list.curselection()[0]
        global select_lib_forinstall
        select_lib_forinstall = lib_forinstall_list.get(index2)
        name_lib_forinstall.set(select_lib_forinstall)

        connection_database = sqlite3.connect("data.db")
        cursor = connection_database.cursor()


        cursor.execute(f'SELECT * FROM lib WHERE name LIKE "{select_lib_forinstall}";')
        lib_forinstall_RESULT = cursor.fetchmany(50)
        InstalledLabel = ""


        if lib_forinstall_RESULT[0][0] in lib_list.get(0,END):
            InstalledLabel = "Installed"
            search_lib_state("OFF")
        else:
            InstalledLabel = "No Installed"
            search_lib_state("ON")

        about_lib_selected_forinstall.set(lib_forinstall_RESULT[0][1].replace("\\n","\n"+f" |{InstalledLabel}|"))


        connection_database.close()
def pop_lib_list():
    lib_list.delete(0,END)
def search_lib():
    pop_lib_list()

    system("pip list > tmp.txt")

    LIBSfile = open("tmp.txt", "r")

    lib = LIBSfile.read()
    LIBSfile.close()
    lib_split_line = lib.split("\n")
    libs = []
    for item in lib_split_line:
        libs.append(item.split(" ")[0])

    libs.pop(0)
    libs.pop(0)
    libs.remove("")

    for lib in libs:
        search_name = lib_name_forsearch.get()
        if search_name in lib:
            lib_list.insert(END, lib)

# ==================UI==================

# Label_title = Label(rootwindow, text="Safa Library Manager",bg=color, font=("Tahoma",15))
# Label_title.place(y=0, x=300)


top_installation = LabelFrame(rootwindow, width=400, height=50, text="Install Lib", bg=color, fg=textcolor)
top_installation.place(x=565, y=0)

top_search = LabelFrame(rootwindow, text="Search My Lib", bg=color, fg=textcolor)
top_search.place(x=400, y=0)


lib_name_forsearch = Entry(top_search)
lib_name_forsearch.pack()

btn_search = Button(top_search, text="Search", command=search_lib)
btn_search.pack()


lib_name_forinstall = Entry(top_installation, textvariable=name_lib_forinstall)
lib_name_forinstall.pack(side=TOP)

btn_install_lib = Button(top_installation, text="Install", command=install_lib, state="active")
btn_install_lib.pack(side=TOP)



lib_list = Listbox(rootwindow, width=45, height=12)
lib_list.place(x=280, y=100)

load_liblist()

Label(rootwindow, text="Library for python :", bg=color, fg=textcolor).place(x=0, y=75)
Label(rootwindow, text="My library :", bg=color, fg=textcolor).place(x=280, y=75)

lib_forinstall_list = Listbox(rootwindow, width=40, height=12)
lib_forinstall_list.place(x=0, y=100)

lib_forinstall_list.bind("<<ListboxSelect>>", get_selected_lib_forinstall)


value_number_lib_label = StringVar(rootwindow, f"Number Lib: {len(lib_list.get(0,END))}")

Label_number_lib = Label(rootwindow, textvariable=value_number_lib_label, bg=color, fg=textcolor)
Label_number_lib.place(y=250, x=600)

Label_about_lib_selected_forinstall = Label(rootwindow, textvariable=about_lib_selected_forinstall, bg=color, fg=textcolor, wraplength=350)
Label_about_lib_selected_forinstall.place(x=0,y=0)

connection_sql = sqlite3.connect("data.db")

cursor = connection_sql.cursor()

sql = """
CREATE TABLE IF NOT EXISTS lib (
    name VARCHAR (60),
    about VARCHAR (60)
);
"""

cursor.execute(sql)
connection_sql.commit()

cursor.execute("SELECT * FROM lib;")
lib_forinstall = cursor.fetchmany(50)


for item in lib_forinstall:
    lib_forinstall_list.insert(0,item[0])

# connection_sql.commit()

connection_sql.close()



sb1 = Scrollbar(rootwindow)
sb1.place(x=560, y=100)

sb2 = Scrollbar(rootwindow)
sb2.place(x=250, y=100)

lib_list.configure(yscrollcommand=sb1.set)
sb1.configure(command=lib_list.yview)

lib_forinstall_list.configure(yscrollcommand=sb2.set)
sb2.configure(command=lib_forinstall_list.yview)


lib_list.bind("<<ListboxSelect>>", get_selected_lib)

btn_uninstall = Button(rootwindow, text="Uninstall Lib", width=12, command=delete_lib)
btn_uninstall.place(x=600, y=100)

btn_uninstall = Button(rootwindow, text="Reload Lib List", width=12, command=load_liblist)
btn_uninstall.place(x=600, y=150)

btn_uninstall = Button(rootwindow, text="About Lib", width=12, command=about_lib)
btn_uninstall.place(x=600, y=200)


rootwindow.mainloop()
