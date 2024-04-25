import tkinter as tk
from tkinter.font import Font
from Mensajes import Textos

class Convertidor:
    def __init__(self):
        self.convertidor = tk.Tk()

        self.convertidor.title(Textos.titulo)

        #self.convertidor.geometry("900x270")
        self.fuente = Font(root=self.convertidor, family='Arial', size=20)

        self.icono = tk.PhotoImage(file="Recursos/icon.png")
        self.convertidor.iconphoto(True, self.icono)

        self.Texto_n = tk.Label(self.convertidor, font=self.fuente, justify='center', text=Textos.t_0)
        self.Texto_n.grid(column=0, row=0, columnspan=2)

        self.__nombre = tk.StringVar()
        self.Entrada_nombre = tk.Entry(self.convertidor, font=self.fuente, width=30, justify='left', textvariable=self.__nombre)
        self.Entrada_nombre.grid(column=0, row=2)

        self.__separador = tk.StringVar()
        self.Entrada_separador = tk.Entry(self.convertidor, font=self.fuente, width=12, justify='left', textvariable=self.__separador)
        self.Entrada_separador.grid(column=1, row=2)

        self.Boton_entrada = tk.Button(self.convertidor, font=self.fuente, text=Textos.t_2, command=lambda:[self._datos(),self.destruir()])
        self.Boton_entrada.grid(column=0, row=3, columnspan=2)

        self.convertidor.mainloop()
    
    def _datos(self):
        nombre = self.__nombre.get()
        separador = self.__separador.get()[1:-1]
        if separador == "\\t":
            separador = "\t"
        return nombre, separador


    def destruir(self):
        self.convertidor.destroy()


class Exito:
    def __init__(self):
        self.Exito = tk.Tk()

        self.Exito.title(Textos.titulo_exito)

        #self.Exito.geometry("800x100")
        self.fuente = Font(root=self.Exito, family='Arial', size=20)

        self.icono = tk.PhotoImage(file="Recursos/icon.png")
        self.Exito.iconphoto(True, self.icono)

        self.Texto_n = tk.Label(self.Exito, font=self.fuente, justify='center', text=Textos.exito)
        self.Texto_n.grid(column=0, row=0)
        self.Exito.after(2000, self.OcultarVentana)
        self.Exito.mainloop()

    def OcultarVentana(self):
        self.Exito.destroy()

""" n = Convertidor()
name, sep = n._datos()
print(f'{name}, \"{sep}\"') """
