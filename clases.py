import json
import random
import config
from services.receta_service import RecetaService as recetasDBservice

class Ingrediente:
    """Clase que representa un ingrediente."""
    def __init__(self, nombre, cantidad, unidad):
        self.nombre = nombre
        self.cantidad = cantidad
        self.unidad = unidad

    def __str__(self):
        return f"{self.nombre} {self.cantidad} {self.unidad}"

    def __repr__(self):
        return f"Ingrediente({self.nombre}, {self.cantidad}, {self.unidad})"
    
    @classmethod
    def from_list(cls, lista):
        """Constructor de un Ingrediente a partir de una lista.
        
        Siempre esperamos el orden: [nombre, cant, unidad]
        """
        return cls(lista[0], lista[1], lista[2])

    def to_list(self):
        """Devolver una lista con los datos del Ingrediente."""
        return [self.nombre, self.cantidad, self.unidad]

class Receta:
    """Clase que representa una receta."""
    def __init__(self, nombre, ingredientes, preparacion,
                 tiempo_prep, tiempo_coc, fecha_crea=None, id_receta = 0 ):       
        self.nombre = nombre
        self.ingredientes = ingredientes
        self.preparacion = preparacion
        self.tiempo_prep = tiempo_prep
        self.tiempo_coc = tiempo_coc
        self.creacion = fecha_crea
        self.id_receta = id_receta

        
    
    def __repr__(self):
        return "Receta({}, {}, {}, {}, {}, {}, {})".format(self.nombre, self.ingredientes,
                                                       self.preparacion, self.tiempo_coc,
                                                       self.tiempo_prep, self.creacion, self.id_receta)
        
    @classmethod
    def from_dic(cls, dic):
        """Construir una Receta a partir de un diccionario con los datos."""
        
        # TODO: poder recibir los ingredientes como objetos Ingrediente
        ingredientes = Receta.ing_from_list(dic["ingredientes"])
        receta_individual = Receta( dic["nombre"], ingredientes, dic["preparacion"],
                      dic["tiempo_prep"], dic["tiempo_coc"],                      
                      dic["creacion"], dic["id_receta"]
                      )
        
       
        return receta_individual
    @staticmethod
    def ing_from_list(lista):
        """Construir una lista de Ingredientes a partir de una lista de listas"""
        ingredientes = []
        for ing_t in lista:
            ing = list(ing_t)
            ingredientes.append(Ingrediente.from_list(ing))
        return ingredientes

    def ing_to_lista(self):
        """Devolver una cadena listando todos los ingredientes de la receta"""
        return "\n".join([str(ing) for ing in self.ingredientes])

    def to_dict(self):
        """Devolver la receta como un diccionario.
        
        Los ingredientes, que se almacenan como una lista de objetos Ingrediente
        se convierten en una lista de listas con los datos de los ingredientes
        usando el metodo to_list() de la clase Ingrediente."""
        return {"nombre": self.nombre,
                "ingredientes": [ing.to_list() for ing in self.ingredientes],
                "preparacion": self.preparacion, "tiempo_prep": self.tiempo_prep,
                "tiempo_coc": self.tiempo_coc, "creacion": self.creacion, "id_receta": self.id_receta}

    def in_ingredientes(self, keyword):
        """Responder si keyword figura o no entre los nombres de todos los ingredientes"""
        for ingrediente in self.ingredientes:
            if keyword in ingrediente.nombre:
                return True
        return False

class Recetario:
    """
    Esta clase mantiene un diccionario que contiene todas las Recetas,
    este debe estar sincronizado con el archivo recetario.json.

    Si hay cambios en el diccionario se deben guardar en el archivo con
    el método guardar.
    """
    archivo = config.data

    def __init__(self, recetas):
        """recetas es un diccionario de Recetas con los nombres como claves."""
       
        self.recetas = recetas
    
    @classmethod
    def from_file(cls):
        """Crear el recetario a partir del archivo JSON.
        
        Lee el archivo y obtiene un diccionario (como esta guardado).
        Las claves (nombres de cada receta) se mantienen, los valores (que son diccionarios)
        se convierten en objetos Receta usando el constructor from_dic() creado en la clase
        Receta.
        """
        with open(cls.archivo) as fo:
            recetario = json.load(fo) # lista de diccionarios
        return cls({key:Receta.from_dic(value) for (key, value) in recetario.items()})
    
    @classmethod
    def from_database(cls):
        """Crear el recetario a partir de la base de datos."""
        data_cruda = recetasDBservice().getAll()
        
        lista_tuplas = data_cruda["recetas"]        
        
        # return cls({key:Receta.from_dic(value) for (key, value) in lista_tuplas})
        return cls({diccionario['nombre']: Receta.from_dic(diccionario) for diccionario in lista_tuplas})

        

    def insertar(self, receta):
        """Insertar una Receta nueva en el diccionario (recetario).
        
        Si la Receta (su nombre) ya existe en el recetario (ya está como clave)
        no se la sobreescribe (esto se puede modificar), sino que se devuelve False.
        Si la Receta no existe (no esta su nombre como clave), se la inserta en el
        diccionario, usando su nombre como clave y la misma Receta como valor. Se
        guardan los cambios en el archivo JSON y se devuelve True.
        """
        if self.existe_receta(receta.nombre):
            return False
        else:
            self.recetas[receta.nombre] = receta
            self.guardar()
            return True

    def crearRecetaEnDB(self, receta):
        """Crear una Receta nueva  en la Base de Datos

        Si la Receta (su nombre) ya existe en el recetario (ya está como clave)
        no se la sobreescribe (esto se puede modificar), sino que se devuelve False.
        Si la Receta no existe (no esta su nombre como clave), se la inserta en el
        diccionario, usando su nombre como clave y la misma Receta como valor. Se
        guardan los cambios en el archivo JSON y se devuelve True.
        """
        nueva_receta = {
            "preparacion": str(receta.preparacion),
             "duracion": receta.tiempo_prep,
              "coccion": receta.tiempo_coc,
              "imagen": "",
               "favorita": 0}
        
        res = recetasDBservice().createOne(receta.nombre, nueva_receta)
        
        return res['status']
    

    def eliminar(self, nombre):
        """Eliminar la Recetea (calve y valor) del diccionario (recetario) si existe.
        
        Si el nombre pasado por parametro no existe como clave en el diccionario
        se devuelve False.
        Si el nombre si existe se elimina del diccionario.
        """
        if not self.existe_receta(nombre):
            print("pasando por no existe")
            return False
        else:
            print("pasando por SI existe")
            del self.recetas[nombre]
            self.guardar()

    def get_receta_del_dia(self):
        """Obtener aleatoriamente una Receta del diccionario."""
        return random.choice(list(self.recetas.values()))

    def existe_receta(self, nombre):
        """Devolver True si la el nombre pasado se encuentra entre las claves."""
        return nombre in self.recetas.keys()
    
    def get_receta(self, nombre):
        """Obtiener una Receta del diccionario dado el nombre."""
       
        return self.recetas.get(nombre)

    def guardar(self):
        """Sobreescribir el archivo recetario.json con el contenido actual del recetario."""
        with open(self.archivo, 'w') as fo:
            json.dump(self.serializable(), fo, indent=4)
    
    def serializable(self):
        """Crear un diccionario similar al original, pero los valores son diccionarios.
        
        El diccionario de recetas de esta clase contiene objetos de tipo Receta.
        Este metodo crea un nuevo diccionario en el que las claves siguen siendo los nombres
        pero los valores no son objetos tipo Receta, sino que son diccionarios.
        Para la conversion se utiliza el metodo to_dict() creado en la clase Receta.
        El fin es hacer que todo el recetario sea un diccionario con objetos serializables.
        """
        return {key:value.to_dict() for (key, value) in self.recetas.items()}

if __name__ == "__main__":

    # pruebas
    recetario = Recetario.from_database()
    for receta in recetario.recetas.values():
        print(receta.nombre)
        print(receta.id_receta)
        print(receta.ing_to_lista())