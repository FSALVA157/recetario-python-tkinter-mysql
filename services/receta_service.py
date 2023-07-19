import os
import json
import mysql.connector
import ast
import datetime
#import ingrediente_receta_service as ingredientesDBService

class RecetaService:
    

    def __init__(self):
        current_dir = os.getcwd()
        config_path = os.path.join(current_dir, 'services/config_data.json')
        with open(config_path ,'r') as config_file:
            data = json.load(config_file)
            self.conn = mysql.connector.connect(**data)           
            self.cur = self.conn.cursor()

    def createOne(self, nombre, receta):
        try:
            new_receta = {**receta, "nombre": nombre}            
            query = """INSERT INTO receta (nombre_receta, preparacion, tiempo_preparacion, tiempo_coccion, imagen, es_favorita)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
            self.cur.execute(query, (new_receta['nombre'],new_receta['preparacion'], new_receta['duracion'], new_receta['coccion'],
                                     new_receta['imagen'], new_receta['favorita']))            
        except Exception as e:
            return {
                "status": False,
                "message": str(e)
            }
        else:            
            self.conn.commit()
        finally:
            self.conn.close()
        return {
                "status": True,
                "message": f"la receta {new_receta['nombre']} ha sido Creada"
            }
    
    def getAll(self):
        try:
            """traer los datos desde la tabla receta"""
            query = """SELECT * FROM receta"""
            self.cur.execute(query)            
            data_tuplas = self.cur.fetchall()          

            """preparar query para obtener ingredientes por receta"""
            query_ingred = """
            SELECT i.nombre_ingrediente, ri.cantidad, i.unidad_medida
            FROM receta_ingrediente AS ri
            INNER JOIN receta AS r
            ON ri.receta_id = r.id_receta 
	        INNER JOIN ingrediente AS i
	        ON ri.ingrediente_id = i.id_ingrediente 
	        WHERE r.id_receta = %s"""
            # self.cur.execute(query_ingred, (1,))            
            # data_ingredientes = self.cur.fetchall()
            #print(data_ingredientes)           
            
            data = []
            for tupla in data_tuplas:
                """manejar la fecha"""
                datetime_obj = tupla[5]
                fecha = datetime_obj.date()  
                """traer la data de la tabla ingredientes"""
                self.cur.execute(query_ingred, (tupla[0],))            
                data_ingredientes = self.cur.fetchall()
                
                data.append(
                     {
                        "id_receta": tupla[0],
                        "nombre": tupla[1],
                        "ingredientes": data_ingredientes,
                        "preparacion": ast.literal_eval(tupla[2]),
                        "tiempo_prep": tupla[3],
                        "tiempo_coc": tupla[4],
                        "creacion": fecha.strftime("%Y-%m-%d")
                 })

            
        except Exception as e:
            return {
                "status": False,
                "message": str(e)
            }        
        finally:
            self.conn.close()
        return {
                "status": True,
                "recetas": data
            }
    
    def getOne(self, id):
        try:
            query = """SELECT * FROM receta WHERE id_receta = %s"""
            self.cur.execute(query, (id,))            
            data = self.cur.fetchall()
        except Exception as e:
            return {
                "status": False,
                "message": str(e)
            }
        # else:            
        #     self.conn.commit()
        finally:
            self.conn.close()
        return {
                "status": True,
                "receta": data
            }
    
    def deleteOne(self, id):
        try:
            query = """DELETE FROM receta WHERE id_receta = %s"""
            self.cur.execute(query, (id,))                        
            num_rows_affected = self.cur.rowcount

            if num_rows_affected == 0:
                respuesta = {
                "status": False,
                "message": "No se encontró el registro con el ID proporcionado."
            }                
            else:                
                respuesta = {
                "status": True,
                "message": "El registro se eliminó exitosamente."
            }
        except Exception as e:
            return {
                "status": False,
                "message": str(e)
            }
        else:            
            self.conn.commit()
        finally:
            self.conn.close()
        return respuesta
    
    def updateOne(self, id, data):
        try:
            query = """UPDATE receta SET nombre_receta=%s, preparacion=%s, tiempo_preparacion=%s, tiempo_coccion=%s            
              WHERE id_receta = %s"""
            new_data = (data['nombre_receta'], data['preparacion'], data['duracion'], data['coccion'], id)
            self.cur.execute(query, new_data)                        
            num_rows_affected = self.cur.rowcount

            if num_rows_affected == 0:
                 respuesta = {
                     "status": False,
                     "message": "No se encontró el registro con el ID proporcionado."
                 }                
            else:
                 respuesta = {
                     "status": True,
                     "message": "El registro ha sido actualizado exitosamente."
                 }                        
            
        except Exception as e:
            return {
                "status": False,
                "message": str(e)
            }
        else:            
            self.conn.commit()
        finally:
            self.conn.close()
        return respuesta
    


if __name__ == "__main__":
    receta_s =  RecetaService()            
    # res =  receta_s.createOne("guiso", {"preparacion": "['agregar carne trozada', 'agregar papa trozada', 'hervir agua']", "duracion": "1 hora", "coccion": "45 minutos", "imagen": "guiso.jpg", "favorita": 0})
    #res = receta_s.getAll()
    #res = receta_s.getOne(1)
    #res = receta_s.deleteOne(3)
    res = receta_s.updateOne(1,{"nombre_receta": "Puchero","preparacion": "['agregar medio choclo', 'carne trozada', 'hervir agua']", "duracion": "40 minutos", "coccion": "30 minutos"
                                #  "imagen": "sopaverd.jpg","favorita": 1
                                 }
                                                                  )
    print(res)

        