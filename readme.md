# Recetario de cocinaç

## Integracion a Base de Datos

* Los servicios implementados se encuentran en la carpeta "services"
* La configuracion de la conexion se encuentra en el archivo config_data.json
* Esta implementacion realiza el CRUD completo y ha sido desarrollada en Sistema Operativo Linux Ubuntu
* Por este motivo puede haber algun problema al ejecutar desde windows pues la ruta del archivo de configuracion en cada servicio requiere que se inviertan las barras por ejemplo
* El DER se encuentra en el propio proyecto "TP_1-DER-recetario-2023.png"
* el .sql de la base de datos tambien esta en la raiz del proyecto "recetariodb.sql"
* Al crear una receta no puedo agregar los ingredientes, solo podre agregarlos al modificar la receta ya creada (esto por falta de tiempo)
* Al agregar un ingrediente lo hace con el campo cantidad predeterminado(tambien por falta de tiempo)
* En caso de desear bajar toda la aplicacion desde Github esta es la direccion "https://github.com/FSALVA157/recetario-python-tkinter-mysql.git"


## Consigna

Se deberá diseñar una aplicación de escritorio con tkinter en la que puedan crear, editar y eliminar recetas de un recetario de cocina electrónico.  

Una receta debe estar compuesta de los siguientes datos:  
* Nombre.  
* Una lista de los ingredientes.  
* Preparación, lista ordenada de pasos a seguir.  
* Tiempo total de preparación (en minutos).  
* Tiempo de cocción (en minutos).  
* Fecha de creación. La fecha y hora en que se creó la receta en la aplicación.  
    
Cada ingrediente debe contar con la siguiente información:  

* Nombre.  
* Unidad de medida.  
* Cantidad.  
 
### Funcionalidades

* Crear una receta.  
* Modificar una receta. Se debe poder modificar al menos el título y los tiempos de preparación y cocción. Idealmente, se deben poder modificar todos los datos (ingredientes, pasos de preparación).  

* Eliminar una receta.  
* Mostrar “receta del día” aleatoria en la ventana principal.  
* Buscar y/o filtrar recetas por:  
  * Nombre.
  * Ingredientes