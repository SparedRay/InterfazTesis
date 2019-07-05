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
from tkinter import ttk
from tkinter import messagebox

import subprocess
import threading



class DatabaseManager:
        

    def __init__(self):
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
    
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Contenedores(ContenedorId integer PRIMARY KEY AUTOINCREMENT,Nombre varchar(255))")
        self.connection.commit()
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Recetas(RecetasId integer PRIMARY KEY AUTOINCREMENT, Nombre varchar(255))")
        self.connection.commit()
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS IngredientesRecetas( IngredientesRecetasId integer PRIMARY KEY AUTOINCREMENT, ContenedorId integer, RecetaId integer, Cantidad integer, CONSTRAINT ContenedorFK FOREIGN KEY (ContenedorId) REFERENCES Contenedores(ContenedorId),CONSTRAINT RecetesFK FOREIGN KEY (RecetaId) REFERENCES Recetas(RecetaId) )")
        self.connection.commit()

        #------------------------------------------
        self.cursor.execute("SELECT * FROM Contenedores")
        contenedores = self.cursor.fetchall()
        
        if(len(contenedores) != 6):
            self.cursor.execute("DELETE FROM Contenedores")   
            self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='Contenedores'")
            initialInfo = ["Contenedor 1","Contenedor 2","Contenedor 3","Contenedor 4","Contenedor 5","Contenedor 6"]

            for info in initialInfo:
                self.cursor.execute("INSERT INTO Contenedores(Nombre) VALUES ('{}')".format(info))
                self.connection.commit()
            
        self.connection.close()#FIN DE CONSTRUCTOR
    
    def ObtenerIngredientes(self):
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM Contenedores")
        contenedores = self.cursor.fetchall()
        print(contenedores)
        self.connection.close()
        return contenedores
        
    def CrearReceta(self,nombre):
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM Recetas Where Nombre = '%s'" % nombre)
        repetido = self.cursor.fetchall()
        if len(repetido) != 0:
            return False
        self.cursor.execute("INSERT INTO Recetas(Nombre) VALUES ('%s')" % nombre)
        self.connection.commit()
        self.connection.close()
        print(self.cursor.lastrowid)
        return self.cursor.lastrowid 
                #~ cursor.execute("SELECT * FROM Contenedores")
        #~ contenedores = cursor.fetchall()


    def AgregarIngrediente(self,dic,recetaId):
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
        for i in dic:
            self.cursor.execute("INSERT INTO IngredientesRecetas(ContenedorId,RecetaId,Cantidad) VALUES (%s,%s,%s)" % (i,recetaId,dic[i]))
            self.connection.commit()
        self.connection.close()
    

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
        #Se nos paso colocar fill=BOTH,expand=1
        #por lo tanto este frame no sigue los estandares de diseño del resto
        
    def RecetasCrearReceta(self):  #MEJORAR LOGICA PARA EVITAR USAR 2 DICCIONARIOS PARA CREAR Y EDITAR
        self.labelReceta.pack_forget()
        self.frameReceta.pack_forget()
        self.labelRecetaCrear.pack()
        self.frameRecetaCrear.pack(fill=BOTH,expand=1)
        ingredientes = self.dbManager.ObtenerIngredientes()
        self.diccionarioIngredientesCrear = { ingredientes[0][1] : ingredientes[0][0], ingredientes[1][1] : ingredientes[1][0], ingredientes[2][1] : ingredientes[2][0], ingredientes[3][1] : ingredientes[3][0], ingredientes[4][1] : ingredientes[4][0], ingredientes[5][1] : ingredientes[5][0] }
        print(self.diccionarioIngredientesCrear)
        print("##### Arriba self.diccionarioIngredientesCrear #####")
        self.comboIngredientesCrear['values'] = (ingredientes[0][1],ingredientes[1][1],ingredientes[2][1],ingredientes[3][1],ingredientes[4][1],ingredientes[5][1])
        self.comboIngredientesCrear.current(0)    
        
    def RecetasEditarReceta(self):
        self.labelReceta.pack_forget()
        self.frameReceta.pack_forget()
        self.labelRecetaEditar.pack()
        self.frameRecetaEditar.pack(fill=BOTH,expand=1)
        ingredientes = self.dbManager.ObtenerIngredientes()
        self.diccionarioIngredientesCrear = { ingredientes[0][1] : ingredientes[0][0], ingredientes[1][1] : ingredientes[1][0], ingredientes[2][1] : ingredientes[2][0], ingredientes[3][1] : ingredientes[3][0], ingredientes[4][1] : ingredientes[4][0], ingredientes[5][1] : ingredientes[5][0] }
        self.comboIngredientesCrear['values'] = (ingredientes[0][1],ingredientes[1][1],ingredientes[2][1],ingredientes[3][1],ingredientes[4][1],ingredientes[5][1])
        self.comboIngredientesCrear.current(0)  

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
            
    #CRUD RECETAS    
    
    def EliminarItemListbox(self,lista):
        texto = lista.get(ACTIVE)
        busqueda = texto.find(" " + chr(0),0,len(texto))
        key = texto[:busqueda]
        del self.diccionarioIngredientes[key]
        print(self.diccionarioIngredientes)
        lista.delete(ACTIVE)
        #~ print(lista.curselection())
    
    def MostrarIngredientes(self,lista):
        lista.delete(0,'end')
        for i in self.diccionarioIngredientes:
            #~ print i, d[i]
             ingredientecantidad = i + " " + chr(0) + " " + self.diccionarioIngredientes[i]
             print(ingredientecantidad)
             lista.insert('end',ingredientecantidad)
             
    
    def AgregarIngrediente(self):
        ingrediente = self.comboIngredientesCrear.get()
        cantidad = self.txtCantidadCrear.get()
        if len(cantidad) == 0:
            return
        self.diccionarioIngredientes[ingrediente] = cantidad
        print(self.diccionarioIngredientes)
        print("Arriba se mostro diccionarioIngredientes")
        self.MostrarIngredientes(self.listBoxRecetaActualCrear)
        
        
        
    def CrearReceta(self):
        if len(self.diccionarioIngredientes) == 0:
            messagebox.showerror("Error", "No se puede crear una receta sin ingredientes.")
            return False
        if len(self.txtRecetaNombreCrear.get()) == 0:
            messagebox.showerror("Error", "Debe ingresar el nombre de la receta antes de continuar.")
            return False
        recetaId = self.dbManager.CrearReceta(self.txtRecetaNombreCrear.get()) #CREAMOS LA RECETA
        if recetaId == False:
            messagebox.showerror("Error", "Ya existe una receta con ese nombre.")
            return False
        dic = {} #DICCIONARIO PARA AGREGAR LOS INGREDIENTES DE LA RECETA
        
        for i in self.diccionarioIngredientes: #CICLO PARA RELLENAR DICCIONARIO
            dic[ self.diccionarioIngredientesCrear[ i ] ] = self.diccionarioIngredientes[i]
        print(dic)
        print("Arriba impreso dic")
        self.dbManager.AgregarIngrediente(dic,recetaId)
        #~ self.diccionarioIngredientesCrear
        messagebox.showinfo("Tarea Realizada", "La receta %s ha sido creada correctamente." % self.txtRecetaNombreCrear.get())
        self.RecetasVolver()
            

    def RecetasVolver(self): #para volver a recetas, colocar posteriormente los demas frames
        self.labelRecetaCrear.pack_forget()
        self.frameRecetaCrear.pack_forget()
        self.labelReceta.pack()
        self.frameReceta.pack(fill=BOTH,expand=1)
        

    
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
            
        contenedores = [self.contenedor1Nombre.get(),self.contenedor2Nombre.get(),self.contenedor3Nombre.get(),self.contenedor4Nombre.get(),self.contenedor5Nombre.get(),self.contenedor6Nombre.get()]    
        print(len(contenedores))
        print(len(set(contenedores)))
        if (len(contenedores) == len(set(contenedores))):
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
        else:
            print("iguales")
            messagebox.showerror("Error", "NO pueden existir dos ingredientes con el mismo nombre")
            return
        
    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
        
        
    def __init__(self):
        self.dbManager = DatabaseManager()
        self.tk = Tk()
        self.tk.geometry("480x320")
        self.tk.title("Sistema de Precisión Mixológica para la Preparación de Bebidas Alcohólicas")
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
        self.btnEditarReceta = Button(self.frameReceta, text=self.textoBotonEditarReceta, command=self.RecetasEditarReceta , height = 5, width = 5)
        self.btnEliminarReceta = Button(self.frameReceta, text=self.textoBotonEliminarReceta, command=lambda:self.clicked('Eliminar \n' + 'Receta') , height = 5, width = 5)
        self.btnCrearReceta = Button(self.frameReceta, text=self.textoBotonCrearReceta, command=self.RecetasCrearReceta , height = 5, width = 5)
        self.btnVolverAdmin = Button(self.frameReceta, text="Volver", command=self.AdminVolver)
        self.btnVerReceta.grid(column=0, row=0,padx=5)    
        self.btnEditarReceta.grid(column=1, row=0,padx=5)
        self.btnEliminarReceta.grid(column=2, row=0,padx=5)
        self.btnVolverAdmin.grid(column=3, row=1, pady=10)
        self.btnCrearReceta.grid(column=0, row=1, padx=5)
        
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

        
        #FRAME RECETA-CREAR
        
        #Array para llevar la logica para crear la receta que basicamente poseera ingrediente id.ingrediente y cantidad
        
        self.frameRecetaCrear = Frame(self.tk)
        self.diccionarioIngredientes = {}
        
        self.labelRecetaCrear = Label(self.tk, text="Crear Receta")
        self.labelRecetaCrear.configure (bg="#eaebf1")

        self.frameRecetaCrear.configure (bg="#eaebf1")  
        
        self.labelIngredientesCrear = Label(self.frameRecetaCrear, text="Ingredientes")
        self.labelCantidadCrear = Label(self.frameRecetaCrear, text="Cantidad")
        self.labelRecetaActualCrear = Label(self.frameRecetaCrear, text="Receta Actual")
        self.labelRecetaNombreCrear = Label(self.frameRecetaCrear, text="Nombre de la Receta")
        self.labelIngredientesCrear.configure (bg="#eaebf1")
        self.labelCantidadCrear.configure (bg="#eaebf1")
        self.labelRecetaActualCrear.configure (bg="#eaebf1")
        self.labelRecetaNombreCrear.configure(bg="#eaebf1")
        
        self.labelIngredientesCrear.grid(row=0,column=0,padx=5)
        self.labelCantidadCrear.grid(row=0,column=1)
        self.labelRecetaActualCrear.grid(row=0,column=2)
        self.labelRecetaNombreCrear.grid(row=2,column=0)
        
        self.comboIngredientesCrear = ttk.Combobox(self.frameRecetaCrear,width=16, state="readonly" )
        self.comboIngredientesCrear['values'] = (0,10,20,30,40,50,60,70,80,90,100)
        self.comboIngredientesCrear.grid(row=1, column=0, padx=2,sticky=N)
        self.comboIngredientesCrear.current(1)
        
        self.vcmd = (self.tk.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        
        self.txtCantidadCrear = Entry(self.frameRecetaCrear, width=16, validate = 'key', validatecommand = self.vcmd)     
        self.txtRecetaNombreCrear = Entry(self.frameRecetaCrear, width=16)
        self.txtCantidadCrear.grid(row=1,column=1,padx=2,sticky=N)
        self.txtRecetaNombreCrear.grid(row=3,column=0)
        self.txtCantidadCrear.bind("<FocusIn>", lambda x:self.AbrirTeclado())
        self.txtRecetaNombreCrear.bind("<FocusIn>", lambda x:self.AbrirTeclado())
        
        self.listBoxRecetaActualCrear = Listbox(self.frameRecetaCrear)
        self.listBoxRecetaActualCrear.grid(row=1,column=2)
        

        
        #~ self.listBoxRecetaActualCrear.bind("<Double-Button-1>", lambda: self.EliminarItemListbox(self.listBoxRecetaActualCrear))
        self.listBoxRecetaActualCrear.bind("<Double-Button-1>", lambda x: self.EliminarItemListbox(self.listBoxRecetaActualCrear))
        #~ command=lambda:self.clicked('Eliminar \n' + 'Receta')
        self.btnVolverRecetaCrear = Button(self.frameRecetaCrear, text="Volver", command=self.RecetasVolver )
        self.btnVolverRecetaCrear.grid(row=4,column=2)
        #BOTON AGREGAR ------------------------------------------------------------
        self.btnAgregarRecetaCrear = Button(self.frameRecetaCrear, text="Agregar", command=self.AgregarIngrediente)
        self.btnAgregarRecetaCrear.grid(row=4,column=1)
        #BOTON CREAR -------------------------------------------------------------------
        self.btnCrearRecetaCrear = Button(self.frameRecetaCrear, text="Crear Receta", command=self.CrearReceta, width = 55)
        #~ self.btnCrearRecetaCrear.configure(width=50)
        self.btnCrearRecetaCrear.grid(row=5, column=0,columnspan=3,pady=8)
                
                
#FRAME RECETA-EDITAR(EDITAR EN PROGRESO)
        
        #Array para llevar la logica para crear la receta que basicamente poseera ingrediente id.ingrediente y cantidad
        
        self.frameRecetaEditar = Frame(self.tk)
        
        self.labelRecetaEditar = Label(self.tk, text="Editar Receta")
        self.labelRecetaEditar.configure (bg="#eaebf1")

        self.frameRecetaEditar.configure (bg="#eaebf1")  
        
        self.labelIngredientesEditar = Label(self.frameRecetaEditar, text="Ingredientes")
        self.labelCantidadEditar = Label(self.frameRecetaEditar, text="Cantidad")
        self.labelRecetaActualEditar = Label(self.frameRecetaEditar, text="Receta Actual")
        self.labelRecetaNombreEditar = Label(self.frameRecetaEditar, text="Nombre de la Receta")
        self.labelIngredientesEditar.configure (bg="#eaebf1")
        self.labelCantidadEditar.configure (bg="#eaebf1")
        self.labelRecetaActualEditar.configure (bg="#eaebf1")
        self.labelRecetaNombreEditar.configure(bg="#eaebf1")
        
        self.labelIngredientesEditar.grid(row=0,column=0,padx=5)
        self.labelCantidadEditar.grid(row=0,column=1)
        self.labelRecetaActualEditar.grid(row=0,column=2)
        self.labelRecetaNombreEditar.grid(row=2,column=0)
        
        self.comboIngredientesEditar = ttk.Combobox(self.frameRecetaEditar,width=16, state="readonly" )
        self.comboIngredientesEditar['values'] = (0,10,20,30,40,50,60,70,80,90,100)
        self.comboIngredientesEditar.grid(row=1, column=0, padx=2,sticky=N)
        self.comboIngredientesEditar.current(1)
        
        
        self.txtCantidadEditar = Entry(self.frameRecetaEditar, width=16, validate = 'key', validatecommand = self.vcmd)     
        self.txtRecetaNombreEditar = Entry(self.frameRecetaEditar, width=16)
        self.txtCantidadEditar.grid(row=1,column=1,padx=2,sticky=N)
        self.txtRecetaNombreEditar.grid(row=3,column=0)
        
        self.listBoxRecetaActualEditar = Listbox(self.frameRecetaEditar)
        self.listBoxRecetaActualEditar.grid(row=1,column=2)
        
        self.btnVolverRecetaEditar = Button(self.frameRecetaEditar, text="Volver", command=self.RecetasVolver )
        self.btnVolverRecetaEditar.grid(row=4,column=2)
        #BOTON AGREGAR ------------------------------------------------------------
        self.btnAgregarRecetaEditar = Button(self.frameRecetaEditar, text="Agregar", command=self.AgregarIngrediente)
        self.btnAgregarRecetaEditar.grid(row=4,column=1)
                        
        
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
        
    root = FullScreenWindow()


    root.tk.mainloop()


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
