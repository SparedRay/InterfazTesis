#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2019  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITconnection = sqlite3.connect("DBSystem.sqlite3")NESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import sys
import sqlite3
from tkinter import *


class FullScreenWindow:
    
    def clicked(self,t):
        self.admin = Toplevel(self.tk)
        self.admin.title(t)
        print(t)

    def AdminVentana(self):
        connection = sqlite3.connect("DBSystem.sqlite3")
        cursor = connection.cursor()
    
        cursor.execute("CREATE TABLE IF NOT EXISTS Contenedores(ContenedorId integer PRIMARY KEY AUTOINCREMENT,Nombre varchar(255))")
        connection.commit()
        
        cursor.execute("SELECT * FROM Contenedores")
        contenedores = cursor.fetchall()
        
        if(len(contenedores) != 6):
            cursor.execute("TRUNCATE TABLE Contenedores")    
            initialInfo = ["Contenedor 1","Contenedor 2","Contenedor 3","Contenedor 4","Contenedor 5","Contenedor 6"]

            for info in initialInfo:
                cursor.execute("INSERT INTO Contenedores(Nombre) VALUES ('{}')".format(info))
                connection.commit()
        else:
            cursor.execute("SELECT * FROM Contenedores")
            contenedores = cursor.fetchall()
            self.contenedor1Nombre.set(contenedores[0][1])
            self.contenedor2Nombre.set(contenedores[1][1])
            self.contenedor3Nombre.set(contenedores[2][1])
            self.contenedor4Nombre.set(contenedores[3][1])
            self.contenedor5Nombre.set(contenedores[4][1])
            self.contenedor6Nombre.set(contenedores[5][1])
            
        connection.close()

        self.framePrincipal.pack_forget()
        self.frameAdmin.pack(fill=BOTH,expand=1)
            
            

    
    def AdminVolver(self):
    	self.frameAdmin.pack_forget()
    	self.framePrincipal.pack(fill=BOTH,expand=1)

    def ActualizarContenedores(self):
        connection = sqlite3.connect("DBSystem.sqlite3")
        cursor = connection.cursor()
        cursor.execute("UPDATE Contenedores SET Nombre='{}' WHERE ContenedorId=1".format(self.contenedor1Nombre.get()))
        cursor.execute("UPDATE Contenedores SET Nombre='{}' WHERE ContenedorId=2".format(self.contenedor2Nombre.get()))
        cursor.execute("UPDATE Contenedores SET Nombre='{}' WHERE ContenedorId=3".format(self.contenedor3Nombre.get()))
        cursor.execute("UPDATE Contenedores SET Nombre='{}' WHERE ContenedorId=4".format(self.contenedor4Nombre.get()))
        cursor.execute("UPDATE Contenedores SET Nombre='{}' WHERE ContenedorId=5".format(self.contenedor5Nombre.get()))
        cursor.execute("UPDATE Contenedores SET Nombre='{}' WHERE ContenedorId=6".format(self.contenedor6Nombre.get()))
        connection.commit()
        connection.close()
        
        
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Soy un titulo")
        self.tk.attributes("-zoomed", True)
        self.tk.attributes("-fullscreen", False)
        
        self.contenedor1Nombre = StringVar()
        self.contenedor2Nombre = StringVar()
        self.contenedor3Nombre = StringVar()
        self.contenedor4Nombre = StringVar()
        self.contenedor5Nombre = StringVar()
        self.contenedor6Nombre = StringVar()

       	#etiqueta = Tkinter.Label(root, text="Probando Label")
        self.framePrincipal = Frame(self.tk)
        #~ self.tk.configure (bg="green")
        self.framePrincipal.configure (bg="#eaebf1")
        self.framePrincipal.pack(fill=BOTH,expand=1)
        
        self.frameAdmin = Frame(self.tk)
        self.labelContenedor1 = Label(self.frameAdmin, text="Contenedor 1")
        self.labelContenedor1.grid(column=0, row=1)
        self.labelContenedor2 = Label(self.frameAdmin, text="Contenedor 2")
        self.labelContenedor2.grid(column=0, row=2)
        self.labelContenedor3 = Label(self.frameAdmin, text="Contenedor 3")
        self.labelContenedor3.grid(column=0, row=3)
        self.labelContenedor4 = Label(self.frameAdmin, text="Contenedor 4")
        self.labelContenedor4.grid(column=0, row=4)
        self.labelContenedor5 = Label(self.frameAdmin, text="Contenedor 5")
        self.labelContenedor5.grid(column=0, row=5)
        self.labelContenedor6 = Label(self.frameAdmin, text="Contenedor 6")
        self.labelContenedor6.grid(column=0, row=6)
        self.TextBoxContenedor1=Entry(self.frameAdmin, textvariable= self.contenedor1Nombre)
        self.TextBoxContenedor1.grid(column=1,row=1)
        self.TextBoxContenedor2=Entry(self.frameAdmin, textvariable= self.contenedor2Nombre)
        self.TextBoxContenedor2.grid(column=1,row=2)
        self.TextBoxContenedor3=Entry(self.frameAdmin, textvariable= self.contenedor3Nombre)
        self.TextBoxContenedor3.grid(column=1,row=3)
        self.TextBoxContenedor4=Entry(self.frameAdmin, textvariable= self.contenedor4Nombre)
        self.TextBoxContenedor4.grid(column=1,row=4)
        self.TextBoxContenedor5=Entry(self.frameAdmin, textvariable= self.contenedor5Nombre)
        self.TextBoxContenedor5.grid(column=1,row=5)
        self.TextBoxContenedor6=Entry(self.frameAdmin, textvariable= self.contenedor6Nombre)
        self.TextBoxContenedor6.grid(column=1,row=6)
        self.btn4 = Button(self.frameAdmin, text="Guardar Cambios", command=self.ActualizarContenedores)
        self.btn4.grid(column=2, row=7)
        self.btn3 = Button(self.frameAdmin, text="Volver", command=self.AdminVolver)
        self.btn3.grid(column=2, row=0)
        self.btn1 = Button(self.framePrincipal, text="Admin", command=self.AdminVentana , height = 10, width = 10)
        self.btn2 = Button(self.framePrincipal, text="User", command=lambda:self.clicked("User") , height = 10, width = 10)
        self.btn1.grid(column=0, row=0, padx= 300, pady=100, sticky= "ewns")
        self.btn2.grid(column=1, row=0, pady=100)
        self.btn1.configure (bg="#f1f0ea")
        self.btn2.configure (bg="#f1f0ea")
        self.state = False
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)        
    

        
    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes("-fullscreen", self.state)
        return "break"
        
    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"
        

        

def main(args):
    
    #~ connection = sqlite3.connect("DBSystem.sqlite3")
    #~ cursor = connection.cursor()
    
    #~ cursor.execute("CREATE TABLE IF NOT EXISTS Contenedores(ContenedorId integer PRIMARY KEY AUTOINCREMENT,Nombre varchar(255))")
    
    #~ initialInfo = ["Contenedor 1","Contenedor 2","Contenedor 3","Contenedor 4","Contenedor 5","Contenedor 6"]

    #~ for info in initialInfo:
        #~ cursor.execute("INSERT INTO Contenedores(Nombre) VALUES ('{}')".format(info))

    #~ connection.commit()
    
    root = FullScreenWindow()


    #~ connection.close()
    root.tk.mainloop()


    
    

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
