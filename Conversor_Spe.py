import Func
import os
import errno

def leer(filename, sep):
    extension = filename[-4:]
    if extension == '.spe' or extension == '.Spe':
        _name, carpet = Func.clear_name(filename)
        name = _name[:-4]
        
        try:
            os.mkdir(f'{carpet}{name}')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        lines = []
        with open(filename) as archivo:
            for line in archivo:
                lines.append(line.rstrip())
        tf = open(f'{carpet}{name}/{name}.txt','w')
        sup = '$DATA:'
        
        l_lines = len(lines)
        for i in range(l_lines):
            tf.write(f'#\t{lines[i]}\n')
            if lines[i] == sup:
                break
        tf.write(f'#\t{lines[i+1]}\n')
        
        esp = lines[i+1].find(' ')
        
        n = int(lines[i+1][esp:])
        
        dt = open(f'{carpet}{name}/{name}_datos.dat','w')
        for j in range(n+1):
            tf.write(f'{j}{sep}{lines[i+2+j].strip()}\n')
            p = '' if (j == n) else '\n'
            dt.write(f'{j}{sep}{lines[i+2+j].strip()}{p}')
        
        dt.close()
            
        for k in range(l_lines-(i+2+j)-1):
            p = '' if (k == l_lines-(i+2+j)-2) else '\n'
            tf.write(f'#\t{lines[i+3+j+k]}{p}')
        
        tf.close()