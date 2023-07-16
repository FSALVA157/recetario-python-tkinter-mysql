import os
import json
import mysql.connector


class IngredienteRecetaService:
    

    def __init__(self):
        current_dir = os.getcwd()
        config_path = os.path.join(current_dir, 'services/config_data.json')
        with open(config_path ,'r') as config_file:
            data = json.load(config_file)
            self.conn = mysql.connector.connect(**data)           
            self.cur = self.conn.cursor()

    def createOne(self, data):
        try:
            
            query = """INSERT INTO receta_ingrediente (ingrediente_id, receta_id, cantidad)
                        VALUES (%s, %s, %s)"""
            self.cur.execute(query, (data['ingrediente_id'],data['receta_id'], data['cantidad']))            
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
                "message": f"El enlace ha sido Creado Exitosamente"
            }
    
    def getAll(self):
        try:
            query = """SELECT * FROM receta_ingrediente"""
            self.cur.execute(query)            
            data = self.cur.fetchall()
        except Exception as e:
            return {
                "status": False,
                "message": str(e)
            }        
        finally:
            self.conn.close()
        return {
                "status": True,
                "enlaces": data
            }
    
    def getOne(self, id):
        try:
            query = """SELECT * FROM receta_ingrediente WHERE id_receta_ingrediente = %s"""
            self.cur.execute(query, (id,))            
            data = self.cur.fetchall()
        except Exception as e:
            return {
                "status": False,
                "message": str(e)
            }        
        finally:
            self.conn.close()
        return {
                "status": True,
                "enlace": data
            }
    
    def deleteOne(self, id):
        try:
            query = """DELETE FROM receta_ingrediente WHERE id_receta_ingrediente = %s"""
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
            query = """UPDATE receta_ingrediente SET ingrediente_id=%s, receta_id=%s, cantidad=%s WHERE id_receta_ingrediente = %s"""
            new_data = (data['ingrediente_id'], data['receta_id'],data['cantidad'], id)
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
    
    def getOneByReceta(self, id_receta):
        try:
            query = """
             SELECT i.nombre_ingrediente, ri.cantidad, i.unidad_medida
             FROM receta_ingrediente AS ri
             INNER JOIN receta AS r
             ON ri.receta_id = r.id_receta 
	         INNER JOIN ingrediente AS i
	         ON ri.ingrediente_id = i.id_ingrediente 
	         WHERE r.id_receta = %s"""
            self.cur.execute(query, (id_receta,))            
            data = self.cur.fetchall()
        except Exception as e:
            return {
                "status": False,
                "message": str(e)
            }        
        finally:
            self.conn.close()
        return {
                "status": True,
                "ingredientes": data
            }
    


if __name__ == "__main__":
    ingrediente_s =  IngredienteRecetaService()            
    #res =  enlace_s.createOne({"ingrediente_id": 3, "receta_id": 2, "cantidad": 500})
    #res = ingrediente_s.getAll()
    res = ingrediente_s.getOneByReceta(2)    
    # res = ingrediente_s.getOne(2)
    #res = ingrediente_s.deleteOne(3)
    #res = ingrediente_s.updateOne(16,{"nombre_ingrediente": "caldo de verduras", "unidad_medida": "cubito"})
    print(res)

        