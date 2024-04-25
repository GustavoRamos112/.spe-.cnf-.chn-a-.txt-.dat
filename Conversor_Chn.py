import struct
import numpy as np 
import os
import errno
import Func

class chn_data:
    def __init__(self, filename):
        """ try:
            self.infile = open(filename, "rb")
            self.read_chn_binary()
        except ValueError:
            print('Unable to load file ' + filename) """
        self.infile = open(filename, "rb")
        self.read_chn_binary()

    def read_chn_binary(self):       # We start by reading the 32 byte header
        self.version            = struct.unpack('h', self.infile.read(2))[0]
        self.mca_detector_id    = struct.unpack('h', self.infile.read(2))[0]
        self.segment_number     = struct.unpack('h', self.infile.read(2))[0]
        self.start_time_ss      = self.infile.read(2)
        self.real_time          = struct.unpack('I', self.infile.read(4))[0]
        self.live_time          = struct.unpack('I', self.infile.read(4))[0]
        self.start_date         = self.infile.read(8) #Ascii type date in 
                                #DDMMMYY* where * == 1 means 21th century
        self.start_time_hhmm    = self.infile.read(4)
        self.chan_offset        = struct.unpack('h', self.infile.read(2))[0]
        self.no_channels        = struct.unpack('h', self.infile.read(2))[0]    
        self.hist_array         = np.zeros(self.no_channels) #Init hist_array 

        for i in range(len(self.hist_array)):
            self.hist_array[i]= struct.unpack('I', self.infile.read(4))[0]

        assert struct.unpack('h', self.infile.read(2))[0] == -102

        self.infile.read(2)
        self.en_zero_inter = struct.unpack('f', self.infile.read(4))[0]  
        self.en_slope = struct.unpack('f', self.infile.read(4))[0]
        self.en_quad = struct.unpack('f', self.infile.read(4))[0]
        self.infile.close()

    def write_data_chn(self, filename, sep):
        _name, carpet = Func.clear_name(filename)
        name = _name[:-4]
        try:
            os.mkdir(f'{carpet}{name}')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        tf = open(f'{carpet}{name}/{name}.txt','w')

        tf.writelines(['# Nombre del archivo: ' + filename, 
                       '\n# Version: ' + str(self.version),
                       '\n# ID del detector MCA: ' + str(self.mca_detector_id),
                       f'\n# Hora de inicio: {self.start_time_hhmm[:2]}:{self.start_time_hhmm[2:4]}:{self.start_time_ss}', 
                       f'\n# Fecha de inicio: {self.start_date}', 
                       '\n# Numero de canales: ' + str(self.no_channels), 
                       f'\n# Tiempo vivo: {self.live_time}', 
                       '\n# Tiempo muerto: ' + str(self.real_time), 
                       '\n# El calculo del factor A+Bx+C*x^2',
                       '\n# A : ' + str(self.en_zero_inter), 
                       '\n# B : ' + str(self.en_slope), 
                       '\n# C : ' + str(self.en_quad)])
        
        gh = open(f'{carpet}{name}/{name}_datos.dat','w')
        tf.write(f'\n')
        for i in range(len(self.hist_array)):
            piv = '' if (i+1 == self.no_channels) else '\n'
            tf.write(f'{i}{sep}{int(self.hist_array[i])}{piv}')
            gh.write(f'{i}{sep}{int(self.hist_array[i])}{piv}')
        tf.close()
        gh.close()