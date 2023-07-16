import os
import json
import mysql.connector


class EtiquetaService:
    

    def __init__(self):
        current_dir = os.getcwd()
        config_path = os.path.join(current_dir, 'services/config_data.json')
        with open(config_path ,'r') as config_file:
            data = json.load(config_file)
            self.conn = mysql.connector.connect(**data)           
            self.cur = self.conn.cursor()

    def createOne(self, etiqueta):
        try:
            
            query = """INSERT INTO etiqueta (nombre_etiqueta)
                        VALUES (%s)"""
            self.cur.execute(query, (etiqueta['nombre_etiqueta']))            
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
                "message": f"La etiqueta {etiqueta['nombre_etiqueta']} ha sido Creado Exitosamente"
            }
    
    def getAll(self):
        try:
            query = """SELECT * FROM etiqueta"""
            self.cur.execute(query)            
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
                "etiquetas": data
            }
    
    def getOne(self, id):
        try:
            query = """SELECT * FROM etiqueta WHERE id_etiqueta = %s"""
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
                "etiqueta": data
            }
    
    def deleteOne(self, id):
        try:
            query = """DELETE FROM etiqueta WHERE id_etiqueta = %s"""
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
            query = """UPDATE etiqueta SET nombre_etiqueta=%s  WHERE id_etiqueta = %s"""
            new_data = (data['nombre_etiqueta'], id)
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
    etiqueta_s =  EtiquetaService()            
    res =  etiqueta_s.createOne({"nombre_etiqueta": "pollo"})
    #res = etiqueta_s.getAll()
    #res = etiqueta_s.getOne(2)
    #res = etiqueta_s.deleteOne(3)
    #res = etiqueta_s.updateOne(16,{"nombre_etiqueta": "agridulce"})
    print(res)

        