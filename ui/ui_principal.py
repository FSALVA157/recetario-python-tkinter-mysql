import tkinter as tk
from tkinter import ttk, messagebox
from clases import Recetario
from .ui_receta import RecetaFrame
from services.receta_service import RecetaService as recetasDBservice

class Principal(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)

        self.parent = parent
        
        #self.recetario = Recetario.from_file()
        self.recetario = Recetario.from_database()
       

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=0)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        # titulo
        lbl = ttk.Label(self, text="Recetario de cocina", font=("Arial", 15))
        lbl.grid(row=0, column=0, columnspan=4, pady=5)
        # Receta del día
        self.setup_receta_del_dia()
        # tabla de recetas
        self.setup_tabla()
        # boton: salir
        btn = ttk.Button(self, text="Salir", command=parent.destroy)
        btn.grid(row=3, column=2, columnspan=2, sticky=tk.SE)

    def on_btn_eliminar(self):
        """Eliminar receta seleccionada"""
        nombre = self.get_seleccion()[0]
        id_receta = self.get_seleccion()[1]
        if nombre:
            rta = messagebox.askyesno(message=(f"Realmente desea eliminar "
                                               f"la receta {nombre}"),
                                      title="Eliminar", icon="question")
            if rta:
                print("***VEAMOS EL ID ANTES DE ELIMINAR***")
                print(nombre)
                self.recetario.eliminar(nombre)                
                # for receta in self.recetario.recetas.values():
                #       print(receta.nombre)
                #       print(receta.id_receta)
                #       print(receta.ing_to_lista())
                
                recetasDBservice().deleteOne(id_receta)
                self.cargar_tabla()
                

    def on_btn_nueva(self):
        """Abrir ventana para carga de una nueva receta."""
        self.ventana_receta(receta=None, accion="crear")

    def on_btn_modificar(self):
        nombre = self.get_seleccion()[0]
        if nombre:
            self.ventana_receta(self.recetario.get_receta(nombre),
                                accion="modificar")

    def on_btn_mostrar(self):
        nombre = self.get_seleccion()[0]
        if nombre:
            self.ventana_receta(self.recetario.get_receta(nombre))
    
    def ventana_receta(self, receta, accion="mostrar"):
        """Mostrar ventana con datos de la receta, o en blanco."""
        ventana = tk.Toplevel(self.parent)        
        RecetaFrame(ventana, self.recetario, receta,
                    accion=accion, completado=self.cargar_tabla)

    def get_seleccion(self):
        """Devolver el nombre de la receta seleccionada"""
        seleccion = self.tabla.selection()
        
        if seleccion:
            for item_id in seleccion:
                item = self.tabla.item(item_id) # obtenemos el item y sus datos        
                return (item['values'][0], item['values'][2])
        else:
            messagebox.showinfo(title="Lista de recetas",
                                message="No hay nada seleccionado")
            return None

    def setup_receta_del_dia(self):
        """Crear Frame de receta diaria con sus widgets"""
        frame_receta_dia = ttk.Frame(self, relief="groove")
        frame_receta_dia.grid(row=1, column=0, columnspan=4, sticky=tk.NSEW)
        frame_receta_dia.columnconfigure(0, weight=0)
        frame_receta_dia.columnconfigure(1, weight=0)
        frame_receta_dia.rowconfigure(0, weight=0)
        # labels
        lbl = ttk.Label(frame_receta_dia, text="La receta del día es: ")
        lbl.grid(row=0, column=0, sticky=tk.W, padx=3, pady=3)
        receta_del_dia = self.recetario.get_receta_del_dia()
        lbl = ttk.Label(frame_receta_dia, text=receta_del_dia.nombre)
        lbl.grid(row=0, column=1, sticky=tk.W, padx=3, pady=3)
        # boton mostrar
        btn_mostrar = ttk.Button(frame_receta_dia, text="Ver receta",
                                 command=lambda:self.ventana_receta(receta_del_dia))
        btn_mostrar.grid(row=0,column=2, columnspan=1, padx=3, pady=3, sticky=tk.EW)

    def setup_tabla(self):
        """Crear Frame que contiene la tabla de recetas con sus botones."""
        frame_tabla = ttk.Frame(self, relief="groove", padding=5)
        frame_tabla.grid(row=2, column=0, columnspan=3, sticky=tk.NSEW)
        frame_tabla.columnconfigure(0, weight=1)
        frame_tabla.columnconfigure(1, weight=1)
        frame_tabla.columnconfigure(2, weight=1)
        frame_tabla.columnconfigure(3, weight=1)
        frame_tabla.columnconfigure(4, weight=0)
        frame_tabla.rowconfigure(0, weight=1)
        frame_tabla.rowconfigure(1, weight=1)
        frame_tabla.rowconfigure(2, weight=1)
        # filtra por nombre
        lbl = ttk.Label(frame_tabla, text="Nombre o ingrediente")
        lbl.grid(row=0, column=0, sticky=tk.W, padx=3, pady=3)
        self.fltr_nombre = tk.StringVar()
        fltr_nombre = ttk.Entry(frame_tabla, textvariable=self.fltr_nombre)
        fltr_nombre.grid(row=0, column=1, sticky=tk.W, padx=3, pady=3)
        fltr_nombre.focus_set()
        btn_buscar = ttk.Button(frame_tabla, text="Buscar", command=self.filtrar_listado)
        btn_buscar.grid(row=0, column=2, sticky=tk.W, padx=3, pady=3)
        # listado de recetas
        # crear treeview
        columnas = ('nombre', 'tiempo_prep', 'id')
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas,
                                  show='headings', selectmode="browse")
        self.tabla.grid(row=1, column=0, columnspan=4, sticky=tk.NSEW,
                        padx=5, pady=5)
        self.tabla.heading('nombre', text='Nombre')
        self.tabla.heading('tiempo_prep', text='Tiempo de preparación')
        self.tabla.heading('id', text='Id')        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL,
                                  command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=4, sticky=tk.NS)
        # llenar treeview
        self.cargar_tabla()
        # botones: mostrar, eliminar, crear
        frame_botonera = ttk.Frame(frame_tabla)
        frame_botonera.grid(row=2, column=0, columnspan=5)
        ttk.Button(frame_botonera, text="Mostrar",
                   command=self.on_btn_mostrar).grid(row=0, column=0, padx=3, pady=3, sticky=tk.W)
        ttk.Button(frame_botonera, text="Eliminar",
                   command=self.on_btn_eliminar).grid(row=0, column=1, padx=3, pady=3, sticky=tk.W)
        ttk.Button(frame_botonera, text="Modificar",
                   command=self.on_btn_modificar).grid(row=0, column=2, padx=3, pady=3, sticky=tk.W)
        ttk.Button(frame_botonera, text="Nueva receta",
                   command=self.on_btn_nueva).grid(row=0, column=3, padx=3, pady=3, sticky=tk.E)
    
    def cargar_tabla(self, listado=None):
        """Limpiar el contenido de la tabla y cargarla nuevamente.
        
        Si listado es None se carga la tabla con el contenido del recetario entero.
        Si se pasa el parametro listado, se carga la tabla con el contenido de ese
        listado. Esto se hace para mostrar los resultados de las busquedas (filtrado).
        """
        # limpiar
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        # cargar
        if listado is None:
            self.recetario = Recetario.from_database()
            for receta in self.recetario.recetas.values():                
                self.tabla.insert('', tk.END,
                                values=( receta.nombre, receta.tiempo_prep, receta.id_receta))
        else:
            for receta in listado.values():
                self.tabla.insert('', tk.END,
                                values=( receta.nombre, receta.tiempo_prep, receta.id_receta))
    
    def filtrar_listado(self):
        """Filtrar por nombre de receta o por ingrediente."""
        keyword = self.fltr_nombre.get()
        print("buscando: ", keyword)
        resultado = {}
        for nombre, receta in self.recetario.recetas.items():
            if keyword in nombre:   # busca en los nombres
                resultado[nombre] = receta
            elif receta.in_ingredientes(keyword):   # busca en los ingredientes
                resultado[nombre] = receta
        if len(resultado) > 0:
            self.cargar_tabla(listado=resultado)
        else:
            messagebox.showinfo(message="No se encontraron coincidencias.")