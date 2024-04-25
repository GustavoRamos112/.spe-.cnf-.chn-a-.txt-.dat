import datetime as dt
import Mensajes
import os
import errno

def clear_name(filename):
    if '/' in filename:
        piv = len(filename)
        for i in range(piv):
            if filename[-i-1] == '/':
                break
        name = filename[piv-i:piv]
        carpet = filename[0:piv-i]
    else:
        name = filename
        carpet = ''
    return name, carpet

def Escribir_error(_error):
    
    Crear_carpeta(Mensajes.Errores.carpeta)

    now = dt.datetime.now()

    err_fecha = f'{now.day}_{now.month}_{now.year}__{now.hour}_{now.minute}_{now.second}'
    tp = open(f'{Mensajes.Errores.carpeta}/{err_fecha}.dat', 'w')
    tp.write(_error)
    tp.close()

def Crear_carpeta(carpeta):
    try:
        os.mkdir(f'{carpeta}')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    