class Textos:
    ext = ['.chn', '.spe', '.cnf', '.dat', '.txt']
    titulo = f'Convertidor {ext[0]} o {ext[1]} o {ext[2]} -> {ext[3]} y {ext[4]}'
    t_0 = f'Introduce el nombre del archivo y su extension ({ext[0]} o {ext[1]} o {ext{2}})'
    t_1 = f'Ejemplo{ext[0]} o Ejemplo{ext[1]}'
    t_2 = f'Convertir a {ext[2]} y {ext[3]}'
    titulo_exito = 'Exito'
    exito = 'Archivo convertido con exito'

class Errores:
    carpeta = 'output_error'
    mensaje_error_extension = f'Extension incorrecta, solo se admiten {Textos.ext[0]} o {Textos.ext[1]}'
    mensaje_error_archivo = 'Archivo inexistente, ruta o nombre incorrecto'
