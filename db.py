import sqlite3

class DatabaseManager:

    def __init__(self, dbName):
        self.__name = dbName + '.sqlite3'
        self.__boilerplate()

    def __open(self):
        self.connection = sqlite3.connect(self.__name)
        self.cursor = self.connection.cursor()

    def __close(self):
        self.connection.close()
        self.connection = None
        self.cursor = None

    def __boilerplate(self):
        self.__open()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Contenedores(ContenedorId integer PRIMARY KEY AUTOINCREMENT,Nombre varchar(255), CaracterEspecial varchar(1))")
        self.connection.commit()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Recetas(RecetasId integer PRIMARY KEY AUTOINCREMENT, Nombre varchar(255))")
        self.connection.commit()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS IngredientesRecetas( IngredientesRecetasId integer PRIMARY KEY AUTOINCREMENT, ContenedorId integer, RecetaId integer, Cantidad integer, CONSTRAINT ContenedorFK FOREIGN KEY (ContenedorId) REFERENCES Contenedores(ContenedorId),CONSTRAINT RecetesFK FOREIGN KEY (RecetaId) REFERENCES Recetas(RecetaId) ON DELETE CASCADE)")
        self.connection.commit()

        # ------------------------------------------
        self.cursor.execute("SELECT * FROM Contenedores")
        contenedores = self.cursor.fetchall()

        if(len(contenedores) != 6):
            self.cursor.execute("DELETE FROM Contenedores")
            self.cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='Contenedores'")
            initialInfo = {"Contenedor 1": "A", "Contenedor 2": "B", "Contenedor 3": "C",
                           "Contenedor 4": "D", "Contenedor 5": "E", "Contenedor 6": "F"}
            for contenedor, caracterEspecial in sorted(initialInfo.items()):
                self.cursor.execute("INSERT INTO Contenedores(Nombre,CaracterEspecial) VALUES ('%s','%s')" % (
                    contenedor, caracterEspecial))
                self.connection.commit()

        self.__close()

    def Select(self, table, fields = "*", query = None, join = None):
        self.__open()
        str = "SELECT {} FROM {} "
        if join is not None:
            str += join
        if query is not None:
            str += (" WHERE " + query)
        self.cursor.execute(str.format(fields, table))
        result = self.cursor.fetchall()
        self.__close()
        return result

    def Insert(self, table, fields, values, hold = None):
        self.__open()
        str = "INSERT INTO {} ({}) VALUES ({})"
        self.cursor.execute(str.format(table, fields, values))
        self.connection.commit()
        if hold is not None: return
        id = self.cursor.lastrowid
        self.__close()
        return id

    def Update(self, table, set, query, hold = None):
        self.__open()
        str = "UPDATE {} SET {} WHERE {}"
        self.cursor.execute(str.format(table, set, query))
        if hold is not None: return
        self.connection.commit()
        self.__close()
        return True

    def Delete(self, table, id, primary = None):
        self.__open()
        str = "DELETE FROM {} WHERE {}={}"
        if primary is None:
            primary = table + 'Id'
        self.cursor.execute(str.format(table, primary, id))
        self.connection.commit()
        self.__close()
        return True

    def EliminarReceta(self, id):
        print("DELETE FROM Recetas WHERE RecetasId=%s" % id)
        self.Delete('Recetas', id)
        self.EliminarTodosIngredientes(id)
    
    def EliminarTodosIngredientes(self, id):
        return self.Delete('IngredientesRecetas', id, 'RecetaId')

    def BuscarCaracterEspecial(self, contenedor):
        query = "Nombre = '{}'"
        return self.Select('Contenedores', 'CaracterEspecial', query.format(contenedor))

    def ObtenerIngredientes(self):
        return self.Select('Contenedores')

    def VerReceta(self, id):
        dic = {}
        nombre = self.Select('Recetas', 'Nombre', 'RecetasId = %d' % id)
        ######### AQUI TENEMOS EL NOMBRE DE LA RECETA########
        inner = "INNER JOIN Contenedores ON IngredientesRecetas.ContenedorId = Contenedores.ContenedorId"
        fields = "Contenedores.Nombre, IngredientesRecetas.Cantidad, Contenedores.CaracterEspecial"
        ingredientes = self.Select('IngredientesRecetas', fields, 'IngredientesRecetas.RecetaId = %d' % id, inner)
        ##### AQUI TENEMOS LOS INGREDIENTES #####
        dic["Receta"] = nombre[0][0]
        dic["Ingredientes"] = ingredientes
        return dic

    def ObtenerRecetas(self):
        dic = {}
        recetas = self.Select('Recetas', join='ORDER BY Nombre ASC')
        for id, nombre in recetas:
            dic[nombre] = id
        self.connection.close()
        return dic

    def VerificarNombreEditar(self, id, nombre):
        query = "Nombre = '%s' AND RecetasId != %d" % (nombre, id)
        repetido = self.Select('Recetas', query=query)
        return len(repetido) == 0

    def CrearReceta(self, nombre):
        repetido = self.Select('Recetas', query="Nombre = '%s" % nombre)
        if len(repetido) != 0:
            return False
        id = self.Insert('Recetas', 'Nombre', "'%s'" % nombre)
        return id

    def ActualizarNombreReceta(self, nombre, id):
        set = "Nombre = '%s'" % nombre
        query = "ReceasId = %d" % id
        return self.Update('Recetas', set, query)

    def ActualizarContenedores(self, contenedores):
        self.__open()
        for i in range(0, 5):
            self.Update('Contenedores', "Nombre = '%s'" % contenedores[i], 'ContenedorId = %d' % (i + 1), True)
        self.connection.commit()
        self.__close()
        return True

    def AgregarIngrediente(self, dic, recetaId):
        self.connection = sqlite3.connect("DBSystem.sqlite3")
        self.cursor = self.connection.cursor()
        for i in dic:
            str = "{}, {}, {}"
            self.Insert('IngredientesRecetas', 'ContenedorId, RecetaId, Cantidad', str.format(i, recetaId, dic[i]), True)
        self.__close()
