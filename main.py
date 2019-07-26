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
from bluetooth import *
from time import sleep

import subprocess
import threading



class DatabaseManager:
        

    def __init__(self):

            
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
    
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Contenedores(ContenedorId integer PRIMARY KEY AUTOINCREMENT,Nombre varchar(255), CaracterEspecial varchar(1))")
        self.connection.commit()
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Recetas(RecetasId integer PRIMARY KEY AUTOINCREMENT, Nombre varchar(255))")
        self.connection.commit()
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS IngredientesRecetas( IngredientesRecetasId integer PRIMARY KEY AUTOINCREMENT, ContenedorId integer, RecetaId integer, Cantidad integer, CONSTRAINT ContenedorFK FOREIGN KEY (ContenedorId) REFERENCES Contenedores(ContenedorId),CONSTRAINT RecetesFK FOREIGN KEY (RecetaId) REFERENCES Recetas(RecetaId) ON DELETE CASCADE)")
        self.connection.commit()

        #------------------------------------------
        self.cursor.execute("SELECT * FROM Contenedores")
        contenedores = self.cursor.fetchall()
        
        if(len(contenedores) != 6):
            self.cursor.execute("DELETE FROM Contenedores")   
            self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='Contenedores'")
            initialInfo = {"Contenedor 1" : "A","Contenedor 2" : "B","Contenedor 3" : "C","Contenedor 4" : "D","Contenedor 5" : "E" ,"Contenedor 6" : "F"}
            for contenedor, caracterEspecial in sorted(initialInfo.items()):
                self.cursor.execute("INSERT INTO Contenedores(Nombre,CaracterEspecial) VALUES ('%s','%s')" % (contenedor,caracterEspecial) )
                self.connection.commit()

            
        self.connection.close()#FIN DE CONSTRUCTOR
    
    def EliminarReceta(self,id):
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
        print("DELETE FROM Recetas WHERE RecetasId=%s" % id)
        self.cursor.execute("DELETE FROM Recetas WHERE RecetasId=%s" % id)
        self.cursor.execute("DELETE FROM IngredientesRecetas WHERE RecetaId=%s" % id)
        self.connection.commit()
        self.connection.close()
        
    def BuscarCaracterEspecial(self,contenedor):
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT CaracterEspecial FROM Contenedores WHERE Nombre='%s'" % contenedor)
        caracterEspecial = self.cursor.fetchall()
        print(caracterEspecial)
        self.connection.close()
        return caracterEspecial
    
    def ObtenerIngredientes(self):
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM Contenedores")
        contenedores = self.cursor.fetchall()
        print(contenedores)
        self.connection.close()
        return contenedores
        
    def VerReceta(self,id):
        dic = {}
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT Nombre FROM Recetas WHERE RecetasId = %s" % id)
        nombre = self.cursor.fetchall()
        ######### AQUI TENEMOS EL NOMBRE DE LA RECETA########
        self.cursor.execute("SELECT Contenedores.Nombre, IngredientesRecetas.Cantidad, Contenedores.CaracterEspecial FROM IngredientesRecetas INNER JOIN Contenedores ON IngredientesRecetas.ContenedorId = Contenedores.ContenedorId WHERE IngredientesRecetas.RecetaId=%s" % id)
        ingredientes = self.cursor.fetchall()
        ##### AQUI TENEMOS LOS INGREDIENTES #####
        dic["Receta"] = nombre[0][0]
        dic["Ingredientes"] = ingredientes
        #~ print(dic)
        return dic
        
    def ObtenerRecetas(self):
        dic = {}
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM Recetas ORDER BY Nombre ASC")
        recetas = self.cursor.fetchall()
        for id, nombre in recetas:
            dic[nombre] = id
        self.connection.close()
        return dic
        
    def VerificarNombreEditar(self,id,nombre):  
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
        print(id)
        print(nombre)
        self.cursor.execute("SELECT * FROM Recetas WHERE Nombre = '%s' AND RecetasId != %s" % (nombre,id))
        #~ self.cursor.execute("SELECT * FROM Recetas WHERE Nombre = '" + nombre + "' AND RecetasId != " + str(id))
        repetido = self.cursor.fetchall()
        if len(repetido) != 0:
            return False
        else:
            return True
    def CrearReceta(self,nombre):
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM Recetas WHERE Nombre = '%s'" % nombre)
        repetido = self.cursor.fetchall()
        if len(repetido) != 0:
            return False
        self.cursor.execute("INSERT INTO Recetas(Nombre) VALUES ('%s')" % nombre)
        self.connection.commit()
        self.connection.close()
        print(self.cursor.lastrowid)
        return self.cursor.lastrowid 
        
    def ActualizarNombreReceta(self,nombre,id):
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
        print(nombre)
        print(id)
        self.cursor.execute("UPDATE Recetas SET Nombre = '%s' WHERE RecetasId = %s" % (nombre,id))
        self.connection.commit()        
        self.connection.close()           
        
    def EliminarTodosIngredientes(self,id):
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
        self.cursor.execute("DELETE FROM IngredientesRecetas WHERE RecetaId = %s" % id)
        self.connection.commit()        
        self.connection.close()


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
        
    def Mostrar5s(self):  
        while True:
            sleep(5)
            print("Han pasado 5 segundos")
            
    def AbrirConexionBT(self):
        print("Pase por aqui")
        self.nearby_devices = discover_devices(lookup_names=True)    
        self.s = BluetoothSocket(RFCOMM)
        print(self.nearby_devices)
        print(self.nearby_devices)
        for addr, name in self.nearby_devices:
            if name == "ESP32test":
                service = find_service(address=addr)
                first_match = service[0]
                port = first_match["port"]
                name = first_match["name"]
                host = first_match["host"]
                self.s.connect((host,1))
                self.s.send("CONECTADO")
                print("CONECTADO")
        
        while True:
            server_sock=BluetoothSocket( RFCOMM )
            server_sock.bind(("",PORT_ANY))
            server_sock.listen(1)

            port = server_sock.getsockname()[1]

            uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

            #~ advertise_service( server_sock, "SampleServer",service_id = uuid,service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ],) 
#                   protocols = [ OBEX_UUID ] 
                    
                   
            print("Waiting for connection on RFCOMM channel %d" % port)

            client_sock, client_info = server_sock.accept()
            print("Accepted connection from ", client_info)

            try:
                while True:
                    data = client_sock.recv(1024)
                    if len(data) == 0: break
                    print("received [%s]" % data)
            except IOError:
                pass

            print("disconnected")

            client_sock.close()
            server_sock.close()
            print("all done")
            #~ shellscript = subprocess.Popen(["shellscript.sh"], stdin=subprocess.PIPE)
        #~ self.shellscript = subprocess.Popen(["/home/pi/Documents/Python Pruebas/InterfazTesis/AbrirBT.sh"], stdin=subprocess.PIPE)
        #~ self.hiloBT = subprocess.call("/home/pi/Documents/Python Pruebas/InterfazTesis/AbrirBT.sh", shell=False)


    def EscucharBT(self):
        
        self.AbrirConexionBT()
        #~ while True:
            #~ server_sock=BluetoothSocket( RFCOMM )
            #~ print("DEspues del RFCOMM")

            #~ port = 2
            #~ server_sock.bind(("",port))
            #~ print("Despues del bind")
            #~ server_sock.listen(2)
            #~ print("despues del listen")

            #~ client_sock,address = server_sock.accept()
            #~ print("Accepted connection from " + str(address))

            #~ data = client_sock.recv(1024)
            #~ print("received [%s]" % data)
            #~ print("Aqui en el while")
            #~ sleep(0.1)
            #~ server_sock=BluetoothSocket( L2CAP )
            #~ print("AQui despues de server sock")
 
            #~ port = 0x1001

            #~ server_sock.bind(("",port))
            #~ print("AQui despues de .bind")
            #~ server_sock.listen(1)
            #~ print("Aqui despues de listen 1")

#~ #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ef"
#~ #bluetooth.advertise_service( server_sock, "SampleServerL2CAP",
#~ #                   service_id = uuid,
#~ #                   service_classes = [ uuid ]
#~ #                    )
                   
            #~ client_sock,address = server_sock.accept()
            #~ print("Accepted connection from ",address)

            #~ data = client_sock.recv(1024)
            #~ print("Data received: ", str(data))

            #~ while data:
                #~ print("Aqui en while data")
                #~ client_sock.send('Echo => ' + str(data))
                #~ data = client_sock.recv(1024)
                #~ print("Data received:", str(data))
        

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
        
    def UserVentana(self):
        self.LogicaListaGeneral(self.listboxBebidasDisponibles)
        self.labelBienvenida.pack_forget()
        self.framePrincipal.pack_forget()
        
        self.labelUser.pack()
        self.frameUser.pack(fill=BOTH,expand=1)
        
        self.listboxIngredientes.delete(0, END)
        receta = self.listboxBebidasDisponibles.get(ACTIVE)
        id = self.diccionarioListaGeneral[receta]
        temp = self.dbManager.VerReceta(id)
        for nombre, cantidad, caracterEspecial in temp["Ingredientes"]:
            self.diccionarioIngredientes[nombre] = cantidad
        self.MostrarIngredientes(self.listboxIngredientes)
        self.diccionarioIngredientes = {}

    def LogicaListaGeneral(self,lista):
        self.listboxRecetasGeneral.delete(0,'end')
        self.diccionarioListaGeneral = self.dbManager.ObtenerRecetas()    
        print(self.diccionarioListaGeneral)
        for i in self.diccionarioListaGeneral:
            lista.insert(END,i)            

    def RecetasVentana(self):
        self.LogicaListaGeneral(self.listboxRecetasGeneral)
        self.labelAdmin.pack_forget()                                                                                                                                                                                                                                           
        self.frameAdmin.pack_forget()
        self.labelReceta.pack()
        self.frameReceta.pack() 
        #Se nos paso colocar fill=BOTH,expand=1
        #por lo tanto este frame no sigue los estandares de diseño del resto
        
    def RecetasCrearReceta(self):  
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
        
    def RecetasEditarReceta(self,id):
        self.RecetaId = id
        temp = self.dbManager.VerReceta(id)
        #~ self.diccionarioIngredientes 
        self.txtRecetaNombreEditar.delete(0, END)
        self.txtRecetaNombreEditar.insert(0, temp["Receta"])
        for nombre, cantidad, caracter in temp["Ingredientes"]:
            self.diccionarioIngredientes[nombre] = cantidad
        self.MostrarIngredientes(self.listBoxRecetaActualEditar)
        print(self.diccionarioIngredientes)
        #~ mEntry.delete(0, END) #deletes the current value
        #~ mEntry.insert(0, res)
        self.labelReceta.pack_forget()
        self.frameReceta.pack_forget()
        self.labelRecetaEditar.pack()
        self.frameRecetaEditar.pack(fill=BOTH,expand=1)
        ingredientes = self.dbManager.ObtenerIngredientes()
        self.diccionarioIngredientesCrear = { ingredientes[0][1] : ingredientes[0][0], ingredientes[1][1] : ingredientes[1][0], ingredientes[2][1] : ingredientes[2][0], ingredientes[3][1] : ingredientes[3][0], ingredientes[4][1] : ingredientes[4][0], ingredientes[5][1] : ingredientes[5][0] }
        self.comboIngredientesEditar['values'] = (ingredientes[0][1],ingredientes[1][1],ingredientes[2][1],ingredientes[3][1],ingredientes[4][1],ingredientes[5][1])
        self.comboIngredientesEditar.current(0)  

    def VaciadoContenedorVentana(self):
        self.labelBienvenida.pack_forget()
        self.frameAdmin.pack_forget()
        self.labelAdmin.pack_forget()
        self.frameVaciadoContenedor.pack(fill=BOTH,expand=1)
        ingredientes = self.dbManager.ObtenerIngredientes()
        #~ self.comboIngredientesCrear['values'] = (ingredientes[0][1],ingredientes[1][1],ingredientes[2][1],ingredientes[3][1],ingredientes[4][1],ingredientes[5][1])
        self.labelVaciadoContenedor1['text'] = ingredientes[0][1]
        self.labelVaciadoContenedor2['text'] = ingredientes[1][1]
        self.labelVaciadoContenedor3['text'] = ingredientes[2][1]
        self.labelVaciadoContenedor4['text'] = ingredientes[3][1]
        self.labelVaciadoContenedor5['text'] = ingredientes[4][1]
        self.labelVaciadoContenedor6['text'] = ingredientes[5][1]

    def ContenedorVentana(self):
        self.labelBienvenida.pack_forget()
        connection = sqlite3.connect("DBSystem.sqlite3")
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM Contenedores")
        contenedores = cursor.fetchall()
        
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

    def VerReceta(self,id):
        temp = self.dbManager.VerReceta(id)
        for nombre, cantidad, caracter in temp["Ingredientes"]:
            self.diccionarioIngredientes[nombre] = cantidad
        self.MostrarIngredientes(self.listBoxRecetaVer)
        self.textoLabelVer.set(temp["Receta"])
        self.labelReceta.pack_forget()
        self.frameReceta.pack_forget()
        self.labelRecetaVer.pack()
        self.frameRecetaVer.pack(fill=BOTH,expand=1)
                    
    #CRUD RECETAS    
    
    def EliminarItemListbox(self,lista):
        texto = lista.get(ACTIVE)
        busqueda = texto.find(" " + chr(0),0,len(texto))
        key = texto[:busqueda]
        del self.diccionarioIngredientes[key]
        print(self.diccionarioIngredientes)
        lista.delete(ACTIVE)
        
    
    def EliminarReceta(self):
        receta = self.listboxRecetasGeneral.get(ACTIVE)
        id = self.diccionarioListaGeneral[receta]
        self.dbManager.EliminarReceta(id)
        self.diccionarioListaGeneral = {}
        self.LogicaListaGeneral(self.listboxRecetasGeneral)
        
    def VerBebida(self,lista):
        lista.delete(0, END)
        receta = self.listboxBebidasDisponibles.get(ACTIVE)
        id = self.diccionarioListaGeneral[receta]
        temp = self.dbManager.VerReceta(id)
        for nombre, cantidad, k in temp["Ingredientes"]:
            self.diccionarioIngredientes[nombre] = cantidad
        self.MostrarIngredientes(lista)
        self.diccionarioIngredientes = {}
        return
        

        
    def MostrarIngredientes(self,lista):
        lista.delete(0,'end')
        for i in self.diccionarioIngredientes:
            ingredientecantidad = i + " " + chr(0) + " " + str(self.diccionarioIngredientes[i])
            print(ingredientecantidad)
            lista.insert('end',ingredientecantidad)
    
    def AgregarIngrediente(self,ingrediente,cantidad,lista):

        if len(cantidad) == 0:
            return
        self.diccionarioIngredientes[ingrediente] = cantidad
        print(self.diccionarioIngredientes)
        print("Arriba se mostro diccionarioIngredientes")
        self.MostrarIngredientes(lista)
        
    def EditarReceta(self):
        if len(self.diccionarioIngredientes) == 0:
            messagebox.showerror("Error", "No se puede crear una receta sin ingredientes.")
            return False
        if len(self.txtRecetaNombreEditar.get()) == 0:
            messagebox.showerror("Error", "Debe ingresar el nombre de la receta antes de continuar.")
            return False
        if self.dbManager.VerificarNombreEditar(self.RecetaId,self.txtRecetaNombreEditar.get()) == False:
            messagebox.showerror("Error", "Ya existe una receta con ese nombre.")
            return False 
        self.dbManager.ActualizarNombreReceta(self.txtRecetaNombreEditar.get(),self.RecetaId)
        self.dbManager.EliminarTodosIngredientes(self.RecetaId)
        
        dicc = {} #DICCIONARIO PARA AGREGAR LOS INGREDIENTES DE LA RECETA
        print(self.diccionarioIngredientesCrear)
        print("##############################")
        for i in self.diccionarioIngredientes: #CICLO PARA RELLENAR DICCIONARIO
            print(i)
            print("########################")
            dicc[ self.diccionarioIngredientesCrear[ i ] ] = self.diccionarioIngredientes[i]
        print(dicc)
        print("Arriba impreso dicc")
        self.dbManager.AgregarIngrediente(dicc,self.RecetaId)
        messagebox.showinfo("Tarea Realizada", "La receta %s ha sido actualizada correctamente." % self.txtRecetaNombreEditar.get())
        self.diccionarioIngredientes = {}
        self.txtCantidadEditar.config(validate="none")
        self.txtCantidadEditar.delete(0, END)
        self.txtRecetaNombreEditar.delete(0, END)
        self.listBoxRecetaActualEditar.delete(0, 'end')
        self.txtCantidadEditar.config(validate='key')
        self.RecetasVolver(2)
        return
        
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
        self.diccionarioIngredientes = {}
        self.txtCantidadCrear.config(validate="none")
        self.txtCantidadCrear.delete(0, END)
        self.txtRecetaNombreCrear.delete(0, END)
        self.listBoxRecetaActualCrear.delete(0, 'end')
        self.txtCantidadCrear.config(validate='key')
        self.RecetasVolver(True)


    def RecetasVolver(self,i): 
        self.LogicaListaGeneral(self.listboxRecetasGeneral)
        self.diccionarioIngredientes = {}
        if i == 1:
            self.labelRecetaCrear.pack_forget()
            self.frameRecetaCrear.pack_forget()
        elif i == 2:
            self.labelRecetaEditar.pack_forget()
            self.frameRecetaEditar.pack_forget()
        else:
            self.labelRecetaVer.pack_forget()
            self.frameRecetaVer.pack_forget()
        self.labelReceta.pack()
        self.frameReceta.pack(fill=BOTH,expand=1)
        

    
    def AdminVolver(self):
    	self.frameContenedor.pack_forget()
    	self.frameReceta.pack_forget()
    	self.frameVaciadoContenedor.pack_forget()
        #~ self.frameVaciadoContenedor.pack_forget()
    	self.labelReceta.pack_forget()
        

    	self.labelAdmin.pack()
        
    	self.frameAdmin.pack(fill=BOTH,expand=1)

    #~ def AdminVolverVaciado(self):
    	#~ self.frameContenedor.pack_forget()
    	#~ self.frameReceta.pack_forget()
    	#~ self.labelReceta.pack_forget()

    	#~ self.labelAdmin.pack()
    	#~ self.frameAdmin.pack(fill=BOTH,expand=1)
        
    def PrincipalVolver(self,isAdmin):
        if isAdmin:
            self.frameAdmin.pack_forget()
            self.labelAdmin.pack_forget()
        else:
            self.frameUser.pack_forget()
            self.labelUser.pack_forget()    
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
            
    def MostarV(self):
        print(self.rbOpcionVaciado.get())
    

    def EnviarInformacion(self,trama):
        self.nearby_devices = discover_devices(lookup_names=True)    
        self.s = BluetoothSocket(RFCOMM)
        #~ print(self.nearby_devices)
        for addr, name in self.nearby_devices:
            if name == "ESP32test":
                service = find_service(address=addr)
                first_match = service[0]
                port = first_match["port"]
                name = first_match["name"]
                host = first_match["host"]
                self.s.connect((host,1))
                self.s.send(trama)
        self.s.close()


    def RealizarPedido(self):
        print("Entramos en REALIZAR PEDIDO")
        trama = "" + chr(1); #Inicio de trama 3
        print(self.diccionarioPedido)
        for NombreReceta in self.diccionarioPedido.keys():
            print("Iniciamos primer for")
            id = self.diccionarioListaGeneral[NombreReceta]
            receta = self.dbManager.VerReceta(id)
            for contenedor,cant,caracter in receta["Ingredientes"]:
                #~ el separador entre contenedor y cantidad viene siendo donde esta chr(0)
                #~ 
                print("Muestro caracter")
                print(caracter)
                trama += caracter + chr(29) + str(cant) + chr(29)
            trama += chr(7) + str(self.diccionarioPedido[NombreReceta]) + chr(8)#Aqui agregamos final de receta 1
        trama+= chr(4) # fin de transmision 2
        print(trama)
        self.EnviarInformacion(trama)
        #~ self.diccionarioPedido {Nombre receta : cantidad}
        #~ self.diccionarioListaGeneral {Nombre receta : id}
     
    def AgregarBebidaPedido(self):
        self.diccionarioPedido[ self.listboxBebidasDisponibles.get(ACTIVE) ] = self.txtCantidadBebidas.get()
        print(self.diccionarioPedido)
        print(self.txtCantidadBebidas.get())
        #~ self.listboxPedido.delete(0,'end')
        self.listboxPedido.delete(0, END)
        for i in self.diccionarioPedido:
            print(i)
            self.listboxPedido.insert(END, i + " " + chr(0) + " " + self.diccionarioPedido[i] )
        return

    def EliminarItemPedido(self):
        texto = self.listboxPedido.get(ACTIVE)
        busqueda = texto.find(" "  + chr(0),0,len(texto))
        key = texto[:busqueda]
        del self.diccionarioPedido[key]
        self.listboxPedido.delete(ACTIVE)
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
                       
        #~ self.hiloPrueba = threading.Thread(target=self.EscucharBT)
        #~ self.hiloPrueba.start()
            
            
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
        self.btn2 = Button(self.framePrincipal, text="User", command=self.UserVentana , height = 5, width = 10)
        self.btn1.grid(column=0, row=0, padx=80, pady=40)
        self.btn2.grid(column=1, row=0, padx=10, pady=40)
        self.btn1.configure (bg="#f1f0ea")
        self.btn2.configure (bg="#f1f0ea")

        self.state = False
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)   
        
        #FRAME USUARIO
        self.diccionarioPedido = {} # { "Nombre de bebida unico" : cantidad de bebida  }
        
        self.frameUser = Frame(self.tk)
        self.frameUser.configure(bg="#eaebf1")
        self.labelUser = Label(self.tk, text="Realiza tu pedido")
        self.labelUser.configure(bg="#eaebf1")
        self.labelBebidasDisponibles = Label(self.frameUser, text="Bebidas Disponibles")
        self.labelBebidasDisponibles.grid(row=0,column=0)
        self.labelBebidasDisponibles.configure (bg="#eaebf1")
        self.listboxBebidasDisponibles = Listbox(self.frameUser, height=6, width=18)
        self.listboxBebidasDisponibles.grid(row=1,column=0)
        self.scrollList = Scrollbar(self.frameUser, command= self.listboxBebidasDisponibles.yview)
        self.scrollList.grid(row=1,column=1, sticky="nesw")
        self.listboxBebidasDisponibles.config(yscrollcommand=self.scrollList.set)
        self.labelIngredientes = Label(self.frameUser, text="Ingredientes")
        self.labelIngredientes.grid(row=0,column=2)
        self.labelIngredientes.configure (bg="#eaebf1")
        self.listboxIngredientes = Listbox(self.frameUser, height=6, width=15)
        self.listboxIngredientes.grid(row=1,column=2, padx=15)
        self.labelPedido = Label(self.frameUser, text="Pedido")
        self.labelPedido.grid(row=0,column=3, padx=10)
        self.labelPedido.configure (bg="#eaebf1")
        self.listboxPedido= Listbox(self.frameUser, height=6, width=18)
        self.listboxPedido.grid(row=1,column=3)
        self.scrollList = Scrollbar(self.frameUser, command=  self.listboxPedido.yview)
        self.scrollList.grid(row=1,column=4, sticky="nesw")
        self.listboxPedido.config(yscrollcommand=self.scrollList.set)
        
        self.labelCantidad = Label(self.frameUser, text="Cantidad")
        self.labelCantidad.grid(row=2,column=0)
        self.labelCantidad.configure (bg="#eaebf1")
        self.txtCantidadBebidas = Entry(self.frameUser, width=16)
        self.txtCantidadBebidas.grid(row=3,column=0)
        self.btnAgregar = Button(self.frameUser, text="Agregar" , height = 5, width = 10, command=self.AgregarBebidaPedido)
        self.btnVolverUser = Button(self.frameUser, text="Volver", height = 5, width = 10, command=lambda:self.PrincipalVolver(False))
        self.btnVolverUser.grid(column=3, row=4, pady=10)
        self.btnRealizarPedido = Button(self.frameUser, text="Realizar Pedido", height = 5, width = 10, command=self.RealizarPedido)
        self.btnAgregar.grid(column=0, row=4, pady=10)
        self.btnRealizarPedido.grid(column=2, row=4, pady=10)
        
        self.listboxBebidasDisponibles.bind("<<ListboxSelect>>", lambda y: self.VerBebida(self.listboxIngredientes))
        self.listboxPedido.bind("<Double-Button-1>", lambda x: self.EliminarItemPedido())
        
        #<<ListboxSelect>>
        
        #FRAME ADMIN
        
        self.frameAdmin = Frame(self.tk)
        
        self.labelAdmin = Label(self.tk, text="Admin")
        self.labelAdmin.configure (bg="#eaebf1")

        self.frameAdmin.configure (bg="#eaebf1")  
        
        self.textoVaciadoContenedores= """Vaciado de 
Contenedores
        """
        
        self.btnContenedores = Button(self.frameAdmin, text="Contenedores", command=self.ContenedorVentana , height = 5, width = 10)
        self.btnVaciadoContenedores = Button(self.frameAdmin, text=self.textoVaciadoContenedores, command=self.VaciadoContenedorVentana , height = 5, width = 10)
        self.btnRecetas = Button(self.frameAdmin, text="Recetas", command=self.RecetasVentana , height = 5, width = 10)
        self.btnContenedores.grid(column=0, row=0, padx=23, pady=40)
        self.btnRecetas.grid(column=1, row=0, padx=23, pady=40)
        self.btnVaciadoContenedores.grid(column=2, row=0, padx=23, pady=40)
        self.btnVolverPrincipal = Button(self.frameAdmin, text="Volver", command=lambda:self.PrincipalVolver(True))
        self.btnVolverPrincipal.grid(column=2, row=1)    
        
        #FRAME RECETA
        
        self.frameReceta = Frame(self.tk)
        self.listboxRecetasGeneral = Listbox(self.frameReceta)
        
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
        
        self.btnVerReceta = Button(self.frameReceta, text=self.textoBotonVerReceta, command=lambda:self.VerReceta(self.diccionarioListaGeneral[ self.listboxRecetasGeneral.get(ACTIVE) ]), height = 5, width = 5)
        self.btnEditarReceta = Button(self.frameReceta, text=self.textoBotonEditarReceta, command=lambda:self.RecetasEditarReceta( self.diccionarioListaGeneral[ self.listboxRecetasGeneral.get(ACTIVE) ] ) , height = 5, width = 5)
        self.btnEliminarReceta = Button(self.frameReceta, text=self.textoBotonEliminarReceta, command=self.EliminarReceta , height = 5, width = 5)
        self.btnCrearReceta = Button(self.frameReceta, text=self.textoBotonCrearReceta, command=self.RecetasCrearReceta , height = 5, width = 5)
        self.btnVolverAdmin = Button(self.frameReceta, text="Volver", command=self.AdminVolver)
        self.btnVerReceta.grid(column=0, row=0,padx=5)    
        self.btnEditarReceta.grid(column=1, row=0,padx=5)
        self.btnEliminarReceta.grid(column=2, row=0,padx=5)
        self.btnVolverAdmin.grid(column=3, row=1, pady=10)
        self.btnCrearReceta.grid(column=0, row=1, padx=5)
        
        
        self.listboxRecetasGeneral.grid(column=3, row=0)
        self.scrollList = Scrollbar(self.frameReceta, command= self.listboxRecetasGeneral.yview)
        self.scrollList.grid(column=4, row=0, sticky="nesw")
        self.listboxRecetasGeneral.config(yscrollcommand=self.scrollList.set)
        
        #~ self.listBox.insert(END,'ELEMENTO1')
        
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
        self.comboIngredientesCrear.grid(row=1, column=0, padx=2,sticky=N)
        
        
        self.vcmd = (self.tk.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        
        self.txtCantidadCrear = Entry(self.frameRecetaCrear, width=16, validate = 'key', validatecommand = self.vcmd)     
        self.txtRecetaNombreCrear = Entry(self.frameRecetaCrear, width=16)
        self.txtCantidadCrear.grid(row=1,column=1,padx=2,sticky=N)
        self.txtRecetaNombreCrear.grid(row=3,column=0)
        self.txtCantidadCrear.bind("<FocusIn>", lambda x:self.AbrirTeclado())
        self.txtRecetaNombreCrear.bind("<FocusIn>", lambda x:self.AbrirTeclado())
        
        self.listBoxRecetaActualCrear = Listbox(self.frameRecetaCrear, height=6)
        self.listBoxRecetaActualCrear.grid(row=1,column=2)
        

        
        #~ self.listBoxRecetaActualCrear.bind("<Double-Button-1>", lambda: self.EliminarItemListbox(self.listBoxRecetaActualCrear))
        self.listBoxRecetaActualCrear.bind("<Double-Button-1>", lambda x: self.EliminarItemListbox(self.listBoxRecetaActualCrear))
        #~ command=lambda:self.clicked('Eliminar \n' + 'Receta')
        self.btnVolverRecetaCrear = Button(self.frameRecetaCrear, text="Volver", command=lambda:self.RecetasVolver(1) )
        self.btnVolverRecetaCrear.grid(row=4,column=2)
        #BOTON AGREGAR ------------------------------------------------------------
        self.btnAgregarRecetaCrear = Button(self.frameRecetaCrear, text="Agregar", command=lambda:self.AgregarIngrediente(self.comboIngredientesCrear.get(),self.txtCantidadCrear.get(),self.listBoxRecetaActualCrear))
        self.btnAgregarRecetaCrear.grid(row=4,column=1)
        #BOTON CREAR -------------------------------------------------------------------
        self.btnCrearRecetaCrear = Button(self.frameRecetaCrear, text="Crear Receta", command=self.CrearReceta, width = 55)
        self.btnCrearRecetaCrear.grid(row=5, column=0,columnspan=3,pady=8)
                
                
#FRAME RECETA-EDITAR
        
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
        self.comboIngredientesEditar.grid(row=1, column=0, padx=2,sticky=N)
        
        
        
        self.txtCantidadEditar = Entry(self.frameRecetaEditar, width=16, validate = 'key', validatecommand = self.vcmd)     
        self.txtRecetaNombreEditar = Entry(self.frameRecetaEditar, width=16)
        self.txtCantidadEditar.grid(row=1,column=1,padx=2,sticky=N)
        self.txtRecetaNombreEditar.grid(row=3,column=0)
        
        self.listBoxRecetaActualEditar = Listbox(self.frameRecetaEditar, height=6)
        self.listBoxRecetaActualEditar.grid(row=1,column=2)
        
        self.btnVolverRecetaEditar = Button(self.frameRecetaEditar, text="Volver", command=lambda:self.RecetasVolver(2) )
        self.btnVolverRecetaEditar.grid(row=4,column=2)
        
        self.listBoxRecetaActualEditar.bind("<Double-Button-1>", lambda x: self.EliminarItemListbox(self.listBoxRecetaActualEditar))
        #BOTON AGREGAR ------------------------------------------------------------
        self.btnAgregarRecetaEditar = Button(self.frameRecetaEditar, text="Agregar", command=lambda:self.AgregarIngrediente(self.comboIngredientesEditar.get(),self.txtCantidadEditar.get(),self.listBoxRecetaActualEditar))
        self.btnAgregarRecetaEditar.grid(row=4,column=1)
        #BOTON CREAR -------------------------------------------------------------------
        self.btnEditarRecetaEditar = Button(self.frameRecetaEditar, text="Editar Receta", command=self.EditarReceta, width = 55)
        self.btnEditarRecetaEditar.grid(row=5, column=0,columnspan=3,pady=8)
                       
        #FRAME RECETA-VER
        
        
        self.textoLabelVer = StringVar()
        
        self.frameRecetaVer = Frame(self.tk)
        self.labelRecetaVer = Label(self.tk, text="Ver Receta")
        self.labelRecetaVer.configure (bg="#eaebf1")
        self.frameRecetaVer.configure (bg="#eaebf1") 
        self.labelNombreReceta = Label(self.frameRecetaVer, text="Nombre de la Receta:", anchor="center")
        self.labelNombreReceta.grid(row=0,column=0,padx=30)
        self.labelNombreRecetaReal = Label(self.frameRecetaVer, text="aqui se ve el nombre",textvariable=self.textoLabelVer, height=15, wraplength = 150, padx=20)
        self.labelNombreRecetaReal.grid(row=1,column=0,padx=30)
        self.labelIngredientesVer = Label(self.frameRecetaVer, text="Ingredientes")
        self.labelIngredientesVer.grid(row=0,column=3,padx=55,columnspan=2)
        self.listBoxRecetaVer = Listbox(self.frameRecetaVer, height=6)
        self.listBoxRecetaVer.grid(row=1,column=3, sticky="e",columnspan=2,padx=55)
        self.labelNombreReceta.configure (bg="#eaebf1") 
        self.labelNombreRecetaReal.configure (bg="#eaebf1") 
        self.labelIngredientesVer.configure (bg="#eaebf1") 
        self.btnVolverRecetaVer = Button(self.frameRecetaVer, text="Volver", command=lambda:self.RecetasVolver(3) )
        self.btnVolverRecetaVer.grid(row=4,column=4)
        
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
        
#FRAME VACIADO CONTENEDOR
        self.frameVaciadoContenedor = Frame(self.tk)
        self.labelVaciadoContenedor1 = Label(self.frameVaciadoContenedor, text="Contenedor 1")
        self.labelVaciadoContenedor1.grid(column=0, row=1)
        self.labelVaciadoContenedor2 = Label(self.frameVaciadoContenedor, text="Contenedor 2")
        self.labelVaciadoContenedor2.grid(column=0, row=2)
        self.labelVaciadoContenedor3 = Label(self.frameVaciadoContenedor, text="Contenedor 3")
        self.labelVaciadoContenedor3.grid(column=0, row=3)
        self.labelVaciadoContenedor4 = Label(self.frameVaciadoContenedor, text="Contenedor 4")
        self.labelVaciadoContenedor4.grid(column=0, row=4)
        self.labelVaciadoContenedor5 = Label(self.frameVaciadoContenedor, text="Contenedor 5")
        self.labelVaciadoContenedor5.grid(column=0, row=5)
        self.labelVaciadoContenedor6 = Label(self.frameVaciadoContenedor, text="Contenedor 6")
        self.labelVaciadoContenedor6.grid(column=0, row=6)
        self.btnVolverVaciado = Button(self.frameVaciadoContenedor, text="Volver", command=self.AdminVolver)
        self.btnVolverVaciado.grid(column=2, row=0)     
        self.TextBoxVaciadoContenedor1=Entry(self.frameVaciadoContenedor)
        self.TextBoxVaciadoContenedor1.grid(column=1,row=1)
        self.TextBoxVaciadoContenedor2=Entry(self.frameVaciadoContenedor)
        self.TextBoxVaciadoContenedor2.grid(column=1,row=2)
        self.TextBoxVaciadoContenedor3=Entry(self.frameVaciadoContenedor)
        self.TextBoxVaciadoContenedor3.grid(column=1,row=3)
        self.TextBoxVaciadoContenedor4=Entry(self.frameVaciadoContenedor)
        self.TextBoxVaciadoContenedor4.grid(column=1,row=4)
        self.TextBoxVaciadoContenedor5=Entry(self.frameVaciadoContenedor)
        self.TextBoxVaciadoContenedor5.grid(column=1,row=5)
        self.TextBoxVaciadoContenedor6=Entry(self.frameVaciadoContenedor)
        self.TextBoxVaciadoContenedor6.grid(column=1,row=6)
        
        self.rbOpcionVaciado = IntVar()
        
        self.rbContenedor1 = Radiobutton(self.frameVaciadoContenedor,text="         ",variable=self.rbOpcionVaciado, value=1, command=self.MostarV,indicatoron=False)
        self.rbContenedor2 = Radiobutton(self.frameVaciadoContenedor,text="         ",variable=self.rbOpcionVaciado, value=2, command=self.MostarV,indicatoron=False)
        self.rbContenedor3 = Radiobutton(self.frameVaciadoContenedor,text="         ",variable=self.rbOpcionVaciado, value=3, command=self.MostarV,indicatoron=False)
        self.rbContenedor4 = Radiobutton(self.frameVaciadoContenedor,text="         ",variable=self.rbOpcionVaciado, value=4, command=self.MostarV,indicatoron=False)
        self.rbContenedor5 = Radiobutton(self.frameVaciadoContenedor,text="         ",variable=self.rbOpcionVaciado, value=5, command=self.MostarV,indicatoron=False)
        self.rbContenedor6 = Radiobutton(self.frameVaciadoContenedor,text="         ", variable=self.rbOpcionVaciado, value=6, command=self.MostarV,indicatoron=False)
        self.rbContenedor1.grid(column=2,row=1)
        self.rbContenedor2.grid(column=2,row=2)
        self.rbContenedor3.grid(column=2,row=3)
        self.rbContenedor4.grid(column=2,row=4)
        self.rbContenedor5.grid(column=2,row=5)
        self.rbContenedor6.grid(column=2,row=6)
        
        self.btnVaciado = Button(self.frameVaciadoContenedor, text="Vaciar", command=self.AdminVolver, height = 5, width = 10)
        self.btnVaciado.grid(column=3, row=7) 
        
        self.labelContenedor1ml = Label(self.frameVaciadoContenedor, text="1200 ml")
        self.labelContenedor1ml.grid(column=3, row=1)
        self.labelContenedor2ml = Label(self.frameVaciadoContenedor, text="1200 ml")
        self.labelContenedor2ml.grid(column=3, row=2)
        self.labelContenedor3ml = Label(self.frameVaciadoContenedor, text="1200 ml")
        self.labelContenedor3ml.grid(column=3, row=3)
        self.labelContenedor4ml = Label(self.frameVaciadoContenedor, text="1200 ml")
        self.labelContenedor4ml.grid(column=3, row=4)
        self.labelContenedor5ml = Label(self.frameVaciadoContenedor, text="1200 ml")
        self.labelContenedor5ml.grid(column=3, row=5)
        self.labelContenedor6ml = Label(self.frameVaciadoContenedor, text="1200 ml")
        self.labelContenedor6ml.grid(column=3, row=6)

    

        
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
