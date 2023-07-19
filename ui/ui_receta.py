import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from services.ingrediente_service import IngredienteService as IngredientesServiceDB
from services.ingrediente_receta_service import IngredienteRecetaService as IngredienteRecetaServiceDB
from services.receta_service import RecetaService as RecetasServiceDB

from clases import Receta, Ingrediente

class CargaIngrendiente(ttk.Frame):
    """
    Frame para la ventana para cargar un ingrediente nuevo
    o modificar uno existente.
    """
    def __init__(self, parent, ingredientes, actualizar_listbox, id_receta, ind_mod=None):
        """Inicializar Frame de carga de ingredientes con sus widgets.

        parent: ventana en donde se agrega el frame,
        ingredientes: lista de objetos Ingrediente de la Receta actual.
        actualizar_listbox: callback a la funcion del frame RecetaFrame para
                            actualizar el listbox de ingredientes.
        ind_mod: indice del ingrediente a modificar de la lista de ingredientes.
                 Solo tendrá un valor distinto de None si se esta modificando un
                 ingrediente.
        """
        super().__init__(parent, padding=10)
        self.grid(row=0, column=0, sticky=tk.NSEW)
        parent.focus()
        parent.grab_set()

        self.set_tabla()
        self.cargar_tabla()

        self.ingredientes = ingredientes
        self.actualizar_listbox = actualizar_listbox
        self.ind_mod = ind_mod
        self.ventana = parent
        self.id_receta = id_receta
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

              
       
        ttk.Label(self, text="Ingrediente").grid(row=0, column=0)
        self.in_ing = tk.StringVar()
        ing_entry = ttk.Entry(self, textvariable=self.in_ing)
        ing_entry.grid(row=1, column=0, sticky=tk.EW, padx=3, pady=3)
        ing_entry.focus_set()

        ttk.Label(self, text="Cantidad").grid(row=0, column=1)
        self.in_cant = tk.StringVar()
        cant_entry = ttk.Entry(self, textvariable=self.in_cant)
        cant_entry.grid(row=1, column=1, sticky=tk.EW, padx=3, pady=3)

        ttk.Label(self, text="Unidad").grid(row=0, column=2)
        self.in_uni = tk.StringVar()
        uni_entry = ttk.Entry(self, textvariable=self.in_uni)
        uni_entry.grid(row=1, column=2, sticky=tk.EW, padx=3, pady=3)

        if ind_mod is not None:
            self.in_ing.set(ingredientes[ind_mod].nombre)
            self.in_cant.set(ingredientes[ind_mod].cantidad)
            self.in_uni.set(ingredientes[ind_mod].unidad)

        btn_cancelar = ttk.Button(self, text="Cancelar", command=parent.destroy)
        btn_cancelar.grid(row=2, column=1, sticky=tk.E, padx=3, pady=3)
        btn_aceptar = ttk.Button(self, text="Aceptar", command=self.guardar)
        btn_aceptar.grid(row=2, column=2, sticky=tk.E, padx=3, pady=3)

        
        parent.bind('<Return>', lambda e: btn_aceptar.invoke())


    def guardar(self):
        """Crear nuevo Ingrediente o modificar el Ingrediente actual.

        Si self.ind_mod es None, creamos un objeto Ingrediente nuevo y lo
        agregamos a la lista.
        Si self.ind_mod no es None, es el indice del Ingrediente que se quiere
        modificar.
        """
        tupla_data = self.seleccionar()
        
        """hagamos la peticion para guardar el ingrediente en la db"""
                
        data_para_db = {
            "ingrediente_id": tupla_data[0],
             "receta_id": self.id_receta,
              "cantidad": tupla_data[2],
              }
        res = IngredienteRecetaServiceDB().createOne(data_para_db)
        


        # verificar que no se haya dejado un campo en blanco
        #self.in_cant.set(new_value) 
        self.in_ing.set( tupla_data[1])
        self.in_cant.set( tupla_data[2])
        self.in_uni.set( tupla_data[3])
        if self.in_ing.get() != "" and self.in_cant.get() != "" and self.in_uni.get() != "":
            # aca se debería controlar que la cantidad sea un numero entero
            if self.ind_mod is not None:
                
                # si tenemos el indice del ingrediente a modificar lo hacemos
                self.ingredientes[self.ind_mod].nombre = self.in_ing.get()
                self.ingredientes[self.ind_mod].cantidad = self.in_cant.get()
                self.ingredientes[self.ind_mod].unidad = self.in_uni.get()
                 
            else:
                # si no hay indice, es un ingrediente nuevo, lo agregamos
                ing = Ingrediente.from_list([self.in_ing.get(),
                                            self.in_cant.get(),
                                            self.in_uni.get()])
                self.ingredientes.append(ing)
            self.actualizar_listbox()
            self.ventana.destroy()
        else:
            messagebox.showinfo(message="Debe completar todos los campos.")
    def cargar_tabla(self):
     """Cargar la tabla con los ingredientes de la base de datos         
     """
     #self.vaciar_tabla()
     self.ingredientesdb = IngredientesServiceDB().getAll()
     
     registros = self.ingredientesdb['ingredientes']
     for tupla in registros:
         self.tabla.insert('', tk.END,
                           values=(tupla[0], tupla[1], 1, tupla[2]))
    #  for id_tarea, tarea, completada in registros:
    #      self.tabla.insert('', tk.END,
    #                        values=(id_tarea, tarea, "Si" if completada else "No"))
     
     # ¡Aca escondemos la primera columna 'ID' con los ids de cada tarea!
     self.tabla["displaycolumns"] = ('ingrediente', 'cantidad', 'unidad')      
    def set_tabla(self):
        """Crear la tabla con cuatro columnas, id, ingrediente, cantidad y unidad      
        La columna ID se va a ocultar para que el usuario no la vea,
        ya que no le interesa cual es el id de cada ingrediente.
        De todas formas podemos obeneter el id de cada ingrediente despues.
        """
        columnas = ('id', 'ingrediente', 'cantidad', 'unidad')
        self.tabla = ttk.Treeview(self, columns=columnas,show='headings',
                                  selectmode="browse") # sin multi-seleccion
        self.tabla.grid(row=3, column=0, columnspan=3, sticky=(tk.NSEW))
        scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tabla.yview)
        scroll.grid(row=2, column=3, sticky=tk.NS)
        self.tabla.configure(yscroll=scroll.set)
        self.tabla.heading('id', text='ID')
        self.tabla.heading('ingrediente', text='Ingrediente')
        self.tabla.heading('cantidad', text='Cantidad')
        self.tabla.heading('unidad', text='Unidad') 
    def seleccionar(self):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            #print(item["values"])
            return item["values"]
            # id_tarea = item['values'][0] # id de la tarea obtenida del treeview
            # completada = item['values'][2]
            # if completada == "Si":
            #     messagebox.showinfo(message="La tarea ya estaba completada   ¬¬")
            #     return
            # datos.completar_tarea(id_tarea)
            # messagebox.showinfo(message="Tarea completada :)")
            # self.cargar_tabla()
        else:
            messagebox.showinfo(message="Debe seleccionar un ingrediente primero")

class CargaPaso(ttk.Frame):
    """
    Frame para la ventana para cargar un paso nuevo
    o modificar uno existente.
    """
    def __init__(self, parent, pasos, actualizar_listbox, ind_mod=None):
        """Inicializar Frame de carga de ingredientes con sus widgets.

        parent: ventana en donde se agrega el frame,
        pasos: lista de str con los pasos de la Receta actual.
        actualizar_listbox: callback a la funcion que actualiza el listbox
                            con los pasos de la receta actual.
        ind_mod: si no es None, indica el indice del paso a modificar
                 de la receta actual.
        """
        super().__init__(parent, padding=10)
        self.grid(row=0, column=0, sticky=tk.NSEW)
        parent.focus()
        parent.grab_set()
        self.ventana = parent
        self.pasos = pasos
        self.actualizar_listbox = actualizar_listbox
        self.ind_mod = ind_mod
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        ttk.Label(self, text="Paso de preparación").grid(row=0, column=0, columnspan=3)
        self.in_paso = tk.StringVar()
        if ind_mod is not None:
            self.in_paso.set(pasos[ind_mod])
        paso_entry = ttk.Entry(self, textvariable=self.in_paso, width=80)
        paso_entry.grid(row=1, column=0, columnspan=3, sticky=tk.EW, padx=3, pady=3)
        paso_entry.focus_set()

        btn_cancelar = ttk.Button(self, text="Cancelar", command=parent.destroy)
        btn_cancelar.grid(row=2, column=1, sticky=tk.E, padx=3, pady=3)
        btn_guardar = ttk.Button(self, text="Guardar", command=self.guardar)
        btn_guardar.grid(row=2, column=2, sticky=tk.E, padx=3, pady=3)

        # ponemos como default el boton guardar al presionar Enter
        self.ventana.bind('<Return>', lambda e: btn_guardar.invoke())

    def guardar(self):
        """Crear nuevo paso (str) o modificar el paso actual.

        Si self.ind_mod es None, creamos un se agrega el paso nuevo.
        Si self.ind_mod no es None, es el indice del paso que se quiere
        modificar.
        """
        if self.in_paso.get() != "":
            if self.ind_mod is not None:
                # si tenemos el indice del paso a modificar lo hacemos
                self.pasos[self.ind_mod] = self.in_paso.get()
            else:
                # si no hay indice creamos un nuevo
                self.pasos.append(self.in_paso.get())
            # actualizar lista de pasos
            self.actualizar_listbox()
            self.ventana.destroy()
        else:
            messagebox.showinfo(message="Debe ingresar un paso de la preparación.")

class RecetaFrame(ttk.Frame):
    """
    Frame para la ventana que muestra los datos de una Receta:
    1. Para una Receta existente:
      a. Solo mostrar. Se muestra y no se pueden editar los campos.
      b. Para modificar. Se muestra y se pueden editar los campos.
    2. Cargar una Receta nueva.
    """
    def __init__(self, window, recetario, receta=None,
                 accion="crear", completado=None):
        """Inicializa el Frame de datos de una Receta.

        recetario: es el objeto Recetario, que contiene el diccionario de Recetas
        receta: es el objeto Receta actual (si existe) o es None si se esta
                cargando una receta nueva.
        accion: es uno de 3 valores: "crear", "modificar", "mostrar", indican
                para que se esta creando la ventana.
        completado: es la callback de la ventana Principal que recarga el contenido
                    de la tabla de recetas.
        """
        super().__init__(window, padding=10)
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=tk.NSEW)
        if accion == "modificar":
            window.title("Modificar receta")
        elif accion == "mostrar":
            window.title("Receta")
        elif accion == "crear":
            window.title("Nueva receta")
        window.focus()
        window.grab_set()
        
        self.ventana = window

       
        self.receta = receta
        self.recetario = recetario
        self.completado = completado

        
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=0)

        self.setup_widgets(accion)

    def setup_widgets(self, accion):
        """Crear los widgets del Frame. Entrys, labels, etc. dependiendo de accion"""
        # labels
        ttk.Label(self, text="Receta").grid(row=0, column=0, sticky=tk.W,
                                            padx=3, pady=3)
        ttk.Label(self, text="Tiempo de preparación").grid(row=1, column=0,
                                                           sticky=tk.W, padx=3, pady=3)
        ttk.Label(self, text="Tiempo de cocción").grid(row=2, column=0, sticky=tk.W,
                                                       padx=3, pady=3)
        ttk.Label(self, text="Ingredientes").grid(row=3, column=0, sticky=tk.NW,
                                                  padx=3, pady=3)
        ttk.Label(self, text="Preparación").grid(row=5, column=0, sticky=tk.NW,
                                                 padx=3, pady=3)
        # entrys
        self.in_nombre = tk.StringVar()
        self.in_tcoccion = tk.StringVar()
        self.in_tpreparacion = tk.StringVar()
        self.nombre_entry = ttk.Entry(self, textvariable=self.in_nombre)
        self.nombre_entry.grid(row=0, column=1, columnspan=2,
                               sticky=tk.EW, padx=3, pady=3)
        self.tpreparacion_entry = ttk.Entry(self, textvariable=self.in_tpreparacion)
        self.tpreparacion_entry.grid(row=1, column=1, columnspan=2,
                                     sticky=tk.EW, padx=3, pady=3)
        self.tcoccion_entry = ttk.Entry(self, textvariable=self.in_tcoccion)
        self.tcoccion_entry.grid(row=2, column=1, columnspan=2,
                                 sticky=tk.EW, padx=3, pady=3)
        # listboxes
        self.ing = tk.Variable()
        self.lb_ing = tk.Listbox(self, listvariable=self.ing, height=6,
                                 selectmode=tk.SINGLE, width=40)
        self.lb_ing.grid(row=3, column=1, sticky=tk.NSEW)
        s = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.lb_ing.yview)
        s.grid(row=3, column=2, sticky=tk.NS)
        self.lb_ing.configure(yscrollcommand=s.set)

        self.prep = tk.Variable()
        self.lb_prep = tk.Listbox(self, listvariable=self.prep, height=6,
                                  selectmode=tk.SINGLE, width=40)
        self.lb_prep.grid(row=5, column=1, sticky=tk.NSEW)
        s = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.lb_prep.yview)
        s.grid(row=5, column=2, sticky=tk.NS)
        self.lb_prep.configure(yscrollcommand=s.set)
        # botones
        btn_volver = ttk.Button(self, text="Volver", command=self.ventana.destroy)
        btn_volver.grid(row=7, column=1, columnspan=2, sticky=tk.E, padx=3, pady=3)
        
        if accion == "crear" or accion == "modificar":
            # botones p/agregar ingredientes y pasos de prep
            if(accion == "modificar"):
                marco_btn_ing = ttk.Frame(self)
                marco_btn_ing.grid(row=4, column=0, columnspan=3, sticky=tk.E)
                btn_del_ing = ttk.Button(marco_btn_ing, text="Eliminar", command=self.eliminar_ingrediente)
                btn_del_ing.grid(row=0, column=0, columnspan=1, sticky=tk.E, padx=3, pady=3)
                btn_mod_ing = ttk.Button(marco_btn_ing, text="Modificar", command=self.modificar_ingrediente)
                btn_mod_ing.grid(row=0, column=1, columnspan=1, sticky=tk.E, padx=3, pady=3)

                btn_mas_ing = ttk.Button(marco_btn_ing, text="Agregar ingrediente",
                                     command=self.agregar_ing)            
                btn_mas_ing.grid(row=0, column=2, columnspan=2, sticky=tk.E, padx=3, pady=3)
            # btn_crear_ing = ttk.Button(marco_btn_ing, text="Crear ingrediente",
            #                          command=self.agregar_ing)
            # btn_crear_ing.grid(row=1, column=3, columnspan=3, sticky=tk.E, padx=3, pady=3)

            marco_btn_prep = ttk.Frame(self)
            marco_btn_prep.grid(row=6, column=0, columnspan=3, sticky=tk.E)
            btn_del_prep = ttk.Button(marco_btn_prep, text="Eliminar", command=self.eliminar_paso)
            btn_del_prep.grid(row=0, column=0, columnspan=1, sticky=tk.E, padx=3, pady=3)
            btn_mod_prep = ttk.Button(marco_btn_prep, text="Modificar", command=self.modificar_paso)
            btn_mod_prep.grid(row=0, column=1, columnspan=1, sticky=tk.E, padx=3, pady=3)
            btn_mas_prep = ttk.Button(marco_btn_prep, text="Agregar paso de preparación",
                                      command=self.mas_prep)
            btn_mas_prep.grid(row=0, column=2, columnspan=1, sticky=tk.E, padx=3, pady=3)

            btn_guardar = ttk.Button(self, text="Guardar", command=self.guardar_receta)
            btn_guardar.grid(row=7, column=0, columnspan=1, sticky=tk.E, padx=3, pady=3)
        
        if accion == "crear":
            self.ingredientes = []
            self.preparacion = []
        
        if accion == "modificar":
            self.ingredientes = self.receta.ingredientes
            self.preparacion = self.receta.preparacion

        if accion == "mostrar" or accion == "modificar":
            self.cargar_receta(accion)

    def cargar_receta(self, tipo):
        """Cargar datos de una receta en el frame. Para mostrar o actualizar"""
        #cargar entries
        self.in_nombre.set(self.receta.nombre)
        self.in_tcoccion.set(self.receta.tiempo_coc)
        self.in_tpreparacion.set(self.receta.tiempo_prep)
        # cargar listboxes
        self.ing.set([str(ing) for ing in self.receta.ingredientes])
        self.prep.set(self.receta.preparacion)

        if tipo == "mostrar":
            # hacer los entries no editables
            self.nombre_entry.configure(state='readonly')
            self.tpreparacion_entry.configure(state='readonly')
            self.tcoccion_entry.configure(state='readonly')
    
    def eliminar_ingrediente(self):
        """Eliminar el ingrediente seleccionado en el listbox."""
        seleccionado = self.lb_ing.curselection()  # tupla con indice del elemento
        # print(seleccion)
        if seleccionado:
            ing_seleccionado = self.lb_ing.get(seleccionado)
            # TODO: mostrar cartel de "esta seguro"
            # messagebox.showinfo(message=f"{ing_seleccionado}")
            self.lb_ing.delete(seleccionado)
            self.ingredientes.pop(seleccionado[0]) # sacar el ingrediente de la lista
            
        else:
            messagebox.showinfo(message=f"Debe seleccionar un ingrediente de la lista.")

    def modificar_ingrediente(self):
        """Mostrar ventana para modificar datos de un ingrediente.
        
        Se pasa al Frame la lista de ingredientes, la funcion para actualizar el
        listbox y el indice del ingrediente que se quiere modificar.
        """
        seleccion = self.lb_ing.curselection()
        
        if seleccion:
            ventana_modificar_ing = tk.Toplevel(self.ventana)
            ventana_modificar_ing.title("Modificar ingrediente")
            CargaIngrendiente(ventana_modificar_ing, self.ingredientes,
                              self.actualizar_ingredientes, self.receta.id_receta, seleccion[0])
        else:
            messagebox.showinfo(message=f"Debe seleccionar un ingrediente de la lista.")

    def agregar_ing(self):
        """Abrir ventana para agregar un ingrendiente nuevo.
        
        Se pasa al Frame la lista de ingredientes y la funcion que actualiza
        el listbox.
        """
        ventana_agregar_ing = tk.Toplevel(self.ventana)
        ventana_agregar_ing.title("Agregar ingrediente")
        CargaIngrendiente(ventana_agregar_ing, self.ingredientes, 
                          self.actualizar_ingredientes, self.receta.id_receta)

    def actualizar_ingredientes(self):
        """Actualizar listbox de ingredientes"""
        self.ing.set([str(ing) for ing in self.ingredientes])

    def eliminar_paso(self):
        """Eliminar el paso seleccionado en el listbox."""
        seleccionado = self.lb_prep.curselection()
        
        if seleccionado:
            # paso = self.lb_prep.get(seleccionado)
            # messagebox.showinfo(message=f"{paso}")
            self.lb_prep.delete(seleccionado)
            self.preparacion.pop(seleccionado[0]) # sacar el paso de la lista
            # print(self.preparacion)
        else:
            messagebox.showinfo(message=f"Debe seleccionar un paso de la lista.")

    def modificar_paso(self):
        """Mostrar ventana para modificar datos de un paso.
        
        Se pasa al Frame la lista de pasos, la funcion para actualizar el
        listbox y el indice del paso que se quiere modificar.
        """
        seleccion = self.lb_prep.curselection()
        
        if seleccion:
            ventana_modificar_paso = tk.Toplevel(self.ventana)
            ventana_modificar_paso.title("Modificar paso")
            CargaPaso(ventana_modificar_paso, self.preparacion,
                              self.actualizar_prep, seleccion[0])
        else:
            messagebox.showinfo(message=f"Debe seleccionar un paso de la lista.")

    def mas_prep(self):
        """Abrir ventana para agregar un paso de preparacion.
        
        Se pasa al Frame la lista de los pasos y la funcion que
        actualiza el listbox.
        """
        ventana_mas_prep = tk.Toplevel(self.ventana)
        ventana_mas_prep.title("Agregar paso de preparación")
        CargaPaso(ventana_mas_prep, self.preparacion, self.actualizar_prep)

    def actualizar_prep(self):
        """Actualizar listbox de pasos de preparacion"""
        self.prep.set(self.preparacion)

    def guardar_receta(self):
        """Guardar los datos de la Receta que está cargada en la ventana.

        Si self.receta es None, quiere decir que estamos cargando una receta
        nueva. En tal caso, creamos un nuevo objeto Receta y lo agregamos al
        Recetario (self.recetario).
        Si self.receta no es None, quiere decir que estamos modificando una
        Receta existente.
        Antes de salir (destruir la ventana) ejecutamos el callback completado()
        el cual actualiza la tabla de recetas de la ventana Principal.
        """
        if self.receta is not None:
            # modificar Receta actual
            self.receta.tiempo_prep = self.in_tpreparacion.get()
            self.receta.tiempo_coc = self.in_tcoccion.get()
            # la lista de ingredientes y pasos ya está actualizada en este punto
            # verificar si se cambio el nombre de la receta
            nombre_actual = self.receta.nombre
            nombre_nuevo = self.in_nombre.get()
            if nombre_actual != nombre_nuevo:
                self.receta.nombre = nombre_nuevo
                # el nombre es la clave del diccionario recetario
                # si se modifica, también se debe modificar la clave
                # creamos una nueva clave con el valor de la vieja
                self.recetario.recetas[nombre_nuevo] = self.recetario.recetas.pop(nombre_actual)
            self.recetario.guardar()
            """hagamos la peticion para guardar la receta modificada en la db"""
                
            receta_para_db = {
                "nombre_receta": self.in_nombre.get(),
                 "preparacion": str(self.preparacion),
                  "duracion": self.in_tpreparacion.get(),
                  "coccion": self.in_tcoccion.get()                  
                  }
           
            res = RecetasServiceDB().updateOne(self.receta.id_receta, receta_para_db)
            print(res)
        else:
            # crear nueva Receta
            receta = {}
            receta["nombre"] = self.in_nombre.get()
            receta["ingredientes"] = [ing.to_list() for ing in self.ingredientes]
            receta["preparacion"] = self.preparacion
            receta["tiempo_prep"] = self.in_tpreparacion.get()
            receta["tiempo_coc"] = self.in_tcoccion.get()
            receta["creacion"] = datetime.date.today().isoformat()
            receta["id_receta"] = 6000
            # print(receta)
            self.receta = Receta.from_dic(receta)
            # print(self.receta)
            #self.recetario.insertar(self.receta)
            self.recetario.crearRecetaEnDB(self.receta)
            

        self.completado()   # recarga la tabla principal
        self.ventana.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    RecetaFrame(root).grid()
    root.mainloop()