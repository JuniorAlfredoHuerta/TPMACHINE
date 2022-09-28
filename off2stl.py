import numpy as np
import random

class off_2_stl:
    def __init__(self):
        self.stl = None
        self.facet = None

    def fit(self, filename):
        with open(filename+'.off') as f:
            x = f.readline()
            if x == "OFF\n":
                print("Es un archivo OFF")
            else: 
                print("No es un archivo OFF") 
                return
            a, b, c = [int(x) for x in f.readline().split()] # numero de vertices, caras y bordes
            vertices = np.zeros((a,3), dtype= float) # guarda los vertices del poligono
            self.stl = [] # guarda coordenadas que conforman un triangulo
            vertexlist = [] # guarda vertices 
            self.facet = [] # almacena calculos de la normal
            for i in range(a):
                vertices[i] = f.readline().split()
            for line in f:
                t = ([int(x) for x in line.split()])
                vertexlist.append(t)
            for i in range(b):
                ix = vertexlist[i][0]
                ix = ix -2
                for j in range(ix):
                    self.stl.append([vertexlist[i][1],vertexlist[i][j+2],vertexlist[i][j+3]])
            for i in range(len(self.stl)):
                for j in range(3):
                    p = self.stl[i][j]
                    self.stl[i][j] = vertices[p]
            for i in range(len(self.stl)): # calculo normal: (p2-p1) x (p3-p1)
                p1 = np.array(self.stl[i][0])
                p2 = np.array(self.stl[i][1])
                p3 = np.array(self.stl[i][2])
                N = np.cross(p2-p1, p3-p1)
                self.facet.append(N)
    
    def gen_stl_file(self, newfilename):
        with open(str(newfilename)+'.stl','w') as stlscript:
            stlscript.write('solid Creado por el grupo de Machine Learning\n')
            for i in range(len(self.stl)):
                stlscript.write('facet normal {0} {1} {2}\n'.format(self.facet[i][0],self.facet[i][1],self.facet[i][2]))
                stlscript.write('outer loop\n')
                for j in range(3):
                    stlscript.write("vertex {0} {1} {2}\n".format(self.stl[i][j][0],self.stl[i][j][1],self.stl[i][j][2]))
                stlscript.write('endloop\n')
                stlscript.write('endfacet\n')
            stlscript.write('endsolid\n')


converter = off_2_stl()
print("Make sure the OFF file is in the same folder as the program")
origin_fl = input("Enter the name of the .off file:")
new_fl = input("Enter the name of the converted .stl:")
converter.fit(origin_fl)

converter.gen_stl_file(new_fl)