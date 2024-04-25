import Aplicacion_grafica as Ag
import Conversor_Chn as Co_chn
import Conversor_Spe as Co_Spe
import Conversor_Cnf as Co_cnf
from Func import Escribir_error
import Mensajes

while(True):
    aplicacion = Ag.Convertidor()
    nombre_archivo, separador = aplicacion._datos()

    if nombre_archivo == '':
        break

    err_archivo = False
    try:
        infile = open(nombre_archivo)
        infile.close()
    except Exception:
        err_archivo = True
        Escribir_error(Mensajes.Errores.mensaje_error_archivo)
        pass

    extension = nombre_archivo[-4:]
    
    extensiones = [[".Spe", ".SPE", ".spe"],[".Chn", ".CHN", ".chn"],[".Cnf", ".CNF", ".cnf"]]

    if extension in extensiones[0]:
        Co_Spe.leer(nombre_archivo, separador)
        Ag.Exito()
        break
    elif extension in extensiones[1]:
        archivo = Co_chn.chn_data(nombre_archivo)
        archivo.write_data_chn(nombre_archivo, separador)
        Ag.Exito()
        break
    elif extension in extensiones[2]:
        archivo = Co_cnf.read_cnf_file(nombre_archivo, separador)
        break
    else:
        if err_archivo:
            None
        else:
            Escribir_error(Mensajes.Errores.mensaje_error_extension)