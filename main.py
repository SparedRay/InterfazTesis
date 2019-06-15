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
#PROGRAMA
import sys
import sqlite3
from tkinter import *
import subprocess
import threading



class DatabaseManager:

    def __init__(self):
        connection = sqlite3.connect("DBSystem.sqlite3")
        cursor = connection.cursor()
    
        cursor.execute("CREATE TABLE IF NOT EXISTS Contenedores(ContenedorId integer PRIMARY KEY AUTOINCREMENT,Nombre varchar(255))")
        connection.commit()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS Recetas(RecetasId integer PRIMARY KEY AUTOINCREMENT, Nombre varchar(255))")
        connection.commit()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS IngredientesRecetas( IngredientesRecetasId integer PRIMARY KEY AUTOINCREMENT, ContenedorId integer, RecetaId integer, Cantidad integer, CONSTRAINT ContenedorFK FOREIGN KEY (ContenedorId) REFERENCES Contenedores(ContenedorId),CONSTRAINT RecetesFK FOREIGN KEY (RecetaId) REFERENCES Recetas(RecetaId) )")
        connection.commit()
        #------------------------------------------
        cursor.execute("SELECT * FROM Contenedores")
        contenedores = cursor.fetchall()
        
        if(len(contenedores) != 6):
            cursor.execute("DELETE FROM Contenedores")   
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='Contenedores'")
            initialInfo = ["Contenedor 1","Contenedor 2","Contenedor 3","Contenedor 4","Contenedor 5","Contenedor 6"]

            for info in initialInfo:
                cursor.execute("INSERT INTO Contenedores(Nombre) VALUES ('{}')".format(info))
                connection.commit()
            
        connection.close()#FIN DE CONSTRUCTOR


class FullScreenWindow:
        
    def TecladoVirtual(self):
        self.hiloVentana = subprocess.call("/usr/bin/matchbox-keyboard", shell=False)
        

    def AbrirTeclado(self, event=None):
        self.hilo1 = threading.Thread(target=self.TecladoVirtual)
        self.hilo1.start()
    
    def clicked(self,t):
        #~ print subprocess.Popen("/usr/bin/matchbox-keyboard", shell=True, stdout=subprocess.PIPE).stdout.read()
        #~ return_code = subprocess.call("/usr/bin/matchbox-keyboard", shell=False)  

        self.admin = Toplevel(self.tk)
        self.admin.title(t)
        print(t)

    def AdminVentana(self):
        self.labelBienvenida.pack_forget()
        
        self.framePrincipal.pack_forget()
        self.labelAdmin.pack()
        self.frameAdmin.pack(fill=BOTH,expand=1)

    def RecetasVentana(self):
        self.labelAdmin.pack_forget()
        
        self.frameAdmin.pack_forget()
        self.labelReceta.pack()
        self.frameReceta.pack()
        

    def ContenedorVentana(self):
        self.labelBienvenida.pack_forget()
        connection = sqlite3.connect("DBSystem.sqlite3")
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM Contenedores")
        contenedores = cursor.fetchall()
        
        #~ if(len(contenedores) != 6):
            #~ cursor.execute("TRUNCATE TABLE Contenedores")    
            #~ initialInfo = ["Contenedor 1","Contenedor 2","Contenedor 3","Contenedor 4","Contenedor 5","Contenedor 6"]

            #~ for info in initialInfo:
                #~ cursor.execute("INSERT INTO Contenedores(Nombre) VALUES ('{}')".format(info))
                #~ connection.commit()
        #~ else:
        cursor.execute("SELECT * FROM Contenedores")
        contenedores = cursor.fetchall()
        print(contenedores)
        self.contenedor1Nombre.set(contenedores[0][1])
        self.contenedor2Nombre.set(contenedores[1][1])
        self.contenedor3Nombre.set(contenedores[2][1])
        self.contenedor4Nombre.set(contenedores[3][1])
        self.contenedor5Nombre.set(contenedores[4][1])
        self.contenedor6Nombre.set(contenedores[5][1])
            
        connection.close()

        self.frameAdmin.pack_forget()
        self.labelAdmin.pack_forget()
        self.frameContenedor.pack(fill=BOTH,expand=1)
            
            

    
    def AdminVolver(self):
    	self.frameContenedor.pack_forget()
    	self.frameReceta.pack_forget()
    	self.labelReceta.pack_forget()
        
    	#~ self.labelBienvenida = Label(self.tk, text="Bienvenido")
    	#~ self.labelBienvenida.configure(bg="#eaebf1")
    	self.labelAdmin.pack()
    	self.frameAdmin.pack(fill=BOTH,expand=1)
        
    def PrincipalVolver(self):
        self.frameAdmin.pack_forget()
        self.labelAdmin.pack_forget()
        self.labelBienvenida.pack()
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
        self.tk.geometry("480x320")
        self.tk.title("Soy un titulo")
        #~ self.tk.attributes("-zoomed", True)#PARA TRABAJAR EN LCD
        self.tk.attributes("-zoomed", False)#PARA TRABAJAR EN HDMI
        self.tk.attributes("-fullscreen", False)
        self.tk.configure (bg="#eaebf1")
        
        
        #FRAME PRINCIPAL

        self.labelBienvenida = Label(self.tk, text="Bienvenido")
        self.labelBienvenida.configure (bg="#eaebf1")
        self.labelBienvenida.pack()
        self.framePrincipal = Frame(self.tk)
        self.framePrincipal.configure (bg="#eaebf1")
        self.framePrincipal.pack(fill=BOTH,expand=1)
        
        
        
        
        self.btn1 = Button(self.framePrincipal, text="Admin", command=self.AdminVentana , height = 5, width = 10)
        self.btn2 = Button(self.framePrincipal, text="User", command=lambda:self.clicked("User") , height = 5, width = 10)
        self.btn1.grid(column=0, row=0, padx=80, pady=40)
        self.btn2.grid(column=1, row=0, padx=10, pady=40)
        #~ self.btn1.pack(side= LEFT)
        #~ self.btn2.pack(side= RIGHT)
        self.btn1.configure (bg="#f1f0ea")
        self.btn2.configure (bg="#f1f0ea")
        #~ self.listBox = Listbox(self.framePrincipal)
        #~ self.listBox.grid(column=2, row=1)
        #~ self.scrollList = Scrollbar(self.framePrincipal, command= self.listBox.yview)
        #~ self.scrollList.grid(column=3, row=1, sticky="nesw")
        #~ self.listBox.config(yscrollcommand=self.scrollList.set)
        
        #~ self.listBox.insert(END,'ELEMENTO1')
        #~ self.listBox.insert(END,'ELEMENTO2')
        #~ self.listBox.insert(END,'ELEMENTO3')
        #~ self.listBox.insert(END,'ELEMENTO4')
        #~ self.listBox.insert(END,'ELEMENTO5')
        #~ self.listBox.insert(END,'ELEMENTO6')
        #~ self.listBox.insert(END,'ELEMENTO7')
        #~ self.listBox.insert(END,'ELEMENTO8')
        #~ self.listBox.insert(END,'ELEMENTO9')
        #~ self.listBox.insert(END,'ELEMENTO10')
        #~ self.listBox.insert(END,'ELEMENTO11')
        #~ self.listBox.insert(END,'ELEMENTO12')
        #~ self.listBox.insert(END,'ELEMENTO13')
        #~ self.listBox.insert(END,'ELEMENTO14')
        #~ self.listBox.insert(END,'ELEMENTO15')
        self.state = False
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)   
        
        #FRAME ADMIN
        
        self.frameAdmin = Frame(self.tk)
        
        self.labelAdmin = Label(self.tk, text="Admin")
        self.labelAdmin.configure (bg="#eaebf1")

        self.frameAdmin.configure (bg="#eaebf1")  
        
        
        self.btnContenedores = Button(self.frameAdmin, text="Contenedores", command=self.ContenedorVentana , height = 5, width = 10)
        self.btnRecetas = Button(self.frameAdmin, text="Recetas", command=self.RecetasVentana , height = 5, width = 10)
        self.btnContenedores.grid(column=0, row=0, padx=80, pady=40)
        self.btnRecetas.grid(column=1, row=0, padx=10, pady=40)
        self.btnVolverPrincipal = Button(self.frameAdmin, text="Volver", command=self.PrincipalVolver)
        self.btnVolverPrincipal.grid(column=2, row=1)    
        
        #FRAME RECETA
        
        self.frameReceta = Frame(self.tk)
        
        self.labelReceta = Label(self.tk, text="Recetas")
        self.labelReceta.configure (bg="#eaebf1")

        self.frameReceta.configure (bg="#eaebf1")  
        
        self.textoBotonEliminarReceta = """Eliminar
        Receta        
        """
        self.textoBotonEditarReceta = """Editar
        Receta        
        """
        self.textoBotonVerReceta = """Ver
        Receta        
        """
        
        self.textoBotonCrearReceta = """Crear
        Receta        
        """
        
        self.btnVerReceta = Button(self.frameReceta, text=self.textoBotonVerReceta, command=lambda:self.clicked("Ver /n Receta") , height = 5, width = 5)
        self.btnEditarReceta = Button(self.frameReceta, text=self.textoBotonEditarReceta, command=lambda:self.clicked("Editar Receta") , height = 5, width = 5)
        self.btnEliminarReceta = Button(self.frameReceta, text=self.textoBotonEliminarReceta, command=lambda:self.clicked('Eliminar \n' + 'Receta') , height = 5, width = 5)
        self.btnCrearReceta = Button(self.frameReceta, text=self.textoBotonCrearReceta, command=lambda:self.clicked('Crear Receta') , height = 5, width = 5)
        self.btnVolverAdmin = Button(self.frameReceta, text="Volver", command=self.AdminVolver)
        self.btnVerReceta.grid(column=0, row=0,padx=5)    
        self.btnEditarReceta.grid(column=1, row=0,padx=5)
        self.btnEliminarReceta.grid(column=2, row=0,padx=5)
        self.btnVolverAdmin.grid(column=3, row=1, pady=10)
        self.btnCrearReceta.grid(column=0, row=1
        , padx=5)
        
        
        self.listBox = Listbox(self.frameReceta)
        self.listBox.grid(column=3, row=0)
        self.scrollList = Scrollbar(self.frameReceta, command= self.listBox.yview)
        self.scrollList.grid(column=4, row=0, sticky="nesw")
        self.listBox.config(yscrollcommand=self.scrollList.set)
        
        self.listBox.insert(END,'ELEMENTO1')
        self.listBox.insert(END,'ELEMENTO2')
        self.listBox.insert(END,'ELEMENTO3')
        self.listBox.insert(END,'ELEMENTO4')
        self.listBox.insert(END,'ELEMENTO5')
        self.listBox.insert(END,'ELEMENTO6')
        self.listBox.insert(END,'ELEMENTO7')
        self.listBox.insert(END,'ELEMENTO8')
        self.listBox.insert(END,'ELEMENTO9')
        self.listBox.insert(END,'ELEMENTO10')
        self.listBox.insert(END,'ELEMENTO11')
        self.listBox.insert(END,'ELEMENTO12')
        self.listBox.insert(END,'ELEMENTO13')
        self.listBox.insert(END,'ELEMENTO14')
        self.listBox.insert(END,'ELEMENTO15')
                
        
        
        #FRAME CONTENEDOR
        
        self.contenedor1Nombre = StringVar()
        self.contenedor2Nombre = StringVar()
        self.contenedor3Nombre = StringVar()
        self.contenedor4Nombre = StringVar()
        self.contenedor5Nombre = StringVar()
        self.contenedor6Nombre = StringVar()


        
        self.frameContenedor = Frame(self.tk)
        self.labelContenedor1 = Label(self.frameContenedor, text="Contenedor 1")
        self.labelContenedor1.grid(column=0, row=1)
        self.labelContenedor2 = Label(self.frameContenedor, text="Contenedor 2")
        self.labelContenedor2.grid(column=0, row=2)
        self.labelContenedor3 = Label(self.frameContenedor, text="Contenedor 3")
        self.labelContenedor3.grid(column=0, row=3)
        self.labelContenedor4 = Label(self.frameContenedor, text="Contenedor 4")
        self.labelContenedor4.grid(column=0, row=4)
        self.labelContenedor5 = Label(self.frameContenedor, text="Contenedor 5")
        self.labelContenedor5.grid(column=0, row=5)
        self.labelContenedor6 = Label(self.frameContenedor, text="Contenedor 6")
        self.labelContenedor6.grid(column=0, row=6)
        self.TextBoxContenedor1=Entry(self.frameContenedor, textvariable= self.contenedor1Nombre)
        self.TextBoxContenedor1.grid(column=1,row=1)
        self.TextBoxContenedor2=Entry(self.frameContenedor, textvariable= self.contenedor2Nombre)
        self.TextBoxContenedor2.grid(column=1,row=2)
        self.TextBoxContenedor3=Entry(self.frameContenedor, textvariable= self.contenedor3Nombre)
        self.TextBoxContenedor3.grid(column=1,row=3)
        self.TextBoxContenedor4=Entry(self.frameContenedor, textvariable= self.contenedor4Nombre)
        self.TextBoxContenedor4.grid(column=1,row=4)
        self.TextBoxContenedor5=Entry(self.frameContenedor, textvariable= self.contenedor5Nombre)
        self.TextBoxContenedor5.grid(column=1,row=5)
        self.TextBoxContenedor6=Entry(self.frameContenedor, textvariable= self.contenedor6Nombre)
        self.TextBoxContenedor6.grid(column=1,row=6)
        self.btn4 = Button(self.frameContenedor, text="Guardar Cambios", command=self.ActualizarContenedores)
        self.btn4.grid(column=2, row=7)
        self.btn3 = Button(self.frameContenedor, text="Volver", command=self.AdminVolver)
        self.btn3.grid(column=2, row=0)     
        self.TextBoxContenedor1.bind("<FocusIn>", lambda x:self.AbrirTeclado())
        self.TextBoxContenedor2.bind("<FocusIn>", lambda x:self.AbrirTeclado())
        self.TextBoxContenedor3.bind("<FocusIn>", lambda x:self.AbrirTeclado())
        self.TextBoxContenedor4.bind("<FocusIn>", lambda x:self.AbrirTeclado())
        self.TextBoxContenedor5.bind("<FocusIn>", lambda x:self.AbrirTeclado())
        self.TextBoxContenedor6.bind("<FocusIn>", lambda x:self.AbrirTeclado())
        #~ self.hilo1.terminate()

    

        
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
    
    dbManager = DatabaseManager()
    
    root = FullScreenWindow()


    #~ connection.close()
    root.tk.mainloop()


    
    

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
