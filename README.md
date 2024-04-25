# .spe-.cnf-.chn-a-.txt-.dat
Un convertidor de archivos de ortec (.spe, .chn de maestro y .cnf) a .dat y .txt

## Informacion general
La aplicación fue escrita en Python, en su versión 3.11.1, usando las librerías base de python, Tkinter para la interfaz grafica. Código escrito y depurado por GustavoRamos112 usando como base códigos escritos por messlinger (https://github.com/messlinger) para los archivos cnf y por tegmyr (https://github.com/tegmyr) para los chn, agradeciendo sus aportaciones a la ciencia.

## Como usar
### Archivos
Para introducir un archivo, se tiene que escribir en la entrada de texto de la izquierda el nombre completo al igual que su carpeta de contención (si es que esta se encuentra fuera de la carpeta de la aplicaci´on), por ejemplo, si tenemos un archivo llamado name.chn en la carpeta **C:/User/Ususario/Documentos/Laboratorio** y la aplicacion esta en **C:/User/Ususario/Escritorio/Aplicacion/**, es necesario introducir **C:/User/Ususario/Documentos/Laboratorio/name.chn**, en caso de que el archivo este en la misma carpeta que la aplicación, simplemente se tiene que escribir el nombre, y en ultimo caso que el archivo este en una carpeta en la carpeta de la aplicación, solo se agrega el nombre de la carpeta y el nombre del archivo, por ejemplo: /prub/name.chn.

### Separador
Para la entrada de la derecha, se pone un separador entre comillas, este es el que se encargara de separar los datos al momento de convertir el archivo, por ejemplo, para "\t" los dato se verán como "x  y" (tabulador), otro ejemplo, es para ", ", los datos se verán como "x, y", otro ejemplo absurdo seria para el separador "separador", los datos se verán como "xseparadory" (Esto es para aquellos que usan programas de graficado personalizados y necesitan usar cierto separador), si se deja vació, los datos se verán como "xy".

## Salida de archivos
En la carpeta contenedora del archivo se creara una nueva carpeta del mismo nombre que del archivo (sin extensión, por ejemplo, para un archivo name.chn se genera una carpeta llamada name) y dentro de esta carpeta se generaran dos archivos más, uno .txt donde vendrán todos los datos de archivo, como numero de canales, tiempo vivo, etc. y en el otro, vendrá la información de cada canal separada por el propio separador definido por el usuario.

## Errores
Los errores se generaran en una carpeta aparte llama ourput error, al ser una aplicación sencilla, solo hay dos tipos de errores. 

### Extensión incorrecta
Este error ocurre cuando la extensión del archivo no es la correcta, el programa solo admite estas extensiones: [".Spe", ".SPE", ".spe", ".Chn", ".CHN", ".chn", ".Cnf", ".CNF", ".cnf"]. En caso de que este error ocurra, es necesario revisar la extensión del archivo. 

### Archivo inexistente, ruta o nombre incorrecto
Este error ocurre cuando el archivo no es posible abrirlo, ya sea por que el nombre o la ruta fue mal escrita o el archivo no exista en esa dirección, asi que es recomendado revisar la direccion y nombre del archivo.

### Errores en la conversion
En caso de que la conversión no finalice o este incorrecta, posiblemente sea un error relacionado al archivo, si el error persiste, contactar al correo: **gustavo.angel.fr.96@gmail.com**


