import pandas as pd
import os
import glob
import csv

def vectorDatos(path):

    # Funcion para extraer la subcadena i-esima de la tupla
    def parametroImagen(subCadena):

        Pc = 1  # Probabilidad de ocurrencia 1
        c1, c2, c3, c4 = 0, 0, 0, 0

        if subCadena[0] == 'linea_carril':
            c1 = 1
        elif subCadena[0] == 'linea_emergencia':
            c2 = 1
        elif subCadena[0] == 'borde_izquierdo':
            c3 = 1
        elif subCadena[0] == 'borde_derecho':
            c4 = 1

        # Parametros de las lineas
        x1 = subCadena[1]
        y1 = subCadena[2]
        x2 = subCadena[3]
        y2 = subCadena[4]
        w = subCadena[6]
        h = subCadena[7]

        return [Pc, c1, c2, c3, c4, x1, y1, x2, y2]

    # Cargamos los archivos csv
    files = os.path.join(path, "*.csv")
    files = glob.glob(files)

    # Unimos los .csv's en un solo DataFrame
    df = pd.concat(map(pd.read_csv, files), ignore_index=False)
    df = df[["etiqueta", "x1", "y1", "x2", "y2", "imagen", "w", "h"]]
    df = df.loc[(df['etiqueta'] == 'borde_izquierdo')
                | (df['etiqueta'] == 'borde_derecho')]

    # Creamos una lista con los nombres de las imagenes (sin repetir)
    nombres = df['imagen'].unique()
    repeticionesPorImagen = []
    datosImagenes = []

    for nombre in nombres:
        repeticionesPorImagen.append(list(df['imagen']).count(nombre))

    # Aqui vamos a crear un arreglo con los datos de una misma imagen
    # para recorrernos en todas las imagenes usaremos slices del tipo [n, n + x].
    n = 0
    pivote = 0
    for pivoteTemp in repeticionesPorImagen:
        pivote = pivoteTemp + n
        datosImagenes.append(df[n:pivote].values)
        n += pivoteTemp

    dic_nombre_marcas = {}
    VectorTemp = []
    #flagEmergencia = 0
    #lineasTotales = 7

    # Iteramos sobre el numero de datos de imagenes que tenemos
    # en este caso son 972
    faltan = []
    for i in range(len(datosImagenes)):

        # Aqui vamos a iterar sobre los arreglos de datos de cada imagen

        for j in range(len(datosImagenes[i])):
            if len(datosImagenes[i]) == 2:
                if datosImagenes[i][0][0] == 'borde_izquierdo' and datosImagenes[i][1][0] == 'borde_derecho':
                    for j in range(len(datosImagenes[i])):
                        # Aqui va la prueba para solo el borde
                        # if datosImagenes[i][j][0] == 'borde_izquierdo':
                        # Extraemos la fila de parametros de la imagen dada una etiqueta
                        datosImagenVec = parametroImagen(datosImagenes[i][j])
                        VectorTemp.append(datosImagenVec)

                    nombreImagen = datosImagenes[i][j][5]
                    VectorTemp.append([nombreImagen])
                    dic_nombre_marcas[nombreImagen] = VectorTemp.copy()
                    VectorTemp = []  # Reseteamos nuestro vector temporal
                else:
                    faltan.append(datosImagenes[i][0][5])
                # Banderas de BordeIzquierdo, BordeDerecho y LineaDeEmergencia
                #flagEmergencia = datosImagenVec[2]

        # while len(VectorTemp) < lineasTotales:
            # Aqui verificamos si ya tenemos un registro de linea de emergencia
            # if flagEmergencia == 0:
            #    VectorTemp.append([0, 1, 0, 0, 0, 0, 0, 0, 0])
            #    flagBordeDerecho = 1

            # Aqui verificamos si ya tenemos un registro de borde derecho
            # if flagBordeDerecho == 0:
            #    VectorTemp.append([0, 0, 0, 0, 1, 0, 0, 0, 0])
            #    flagBordeDerecho = 1
            # Aqui verificamos si ya tenemos un registro de borde izquierdo
            # elif flagBordeIzquierdo == 0:
            #    VectorTemp.append([0, 0, 0, 1, 0, 0, 0, 0, 0])
            #    flagBordeIzquierdo = 1

        # Por ultimo agregamos las lineas de carril en las posiciones sobrantes
            # else:
                #VectorTemp.append([0, 0, 1, 0, 0, 0, 0, 0, 0])
                # flagEmergencia = 1 # Dado que ya habremos agregado la linea de Emergancia

        # if flagBordeDerecho == 0:
        #    VectorTemp.append([0, 0, 0, 0, 1, 0, 0, 0, 0])
        # elif flagBordeIzquierdo == 0:
        #    VectorTemp.append([0, 0, 0, 1, 0, 0, 0, 0, 0])

        #nombreImagen = datosImagenes[i][j][5]
        # VectorTemp.append([nombreImagen])
        #dic_nombre_marcas[nombreImagen] = VectorTemp.copy()
        # VectorTemp = []  # Reseteamos nuestro vector temporal

    print(len(faltan))
    print(faltan)
    with open("faltan.csv","w") as f:
        wr = csv.writer(f, delimiter="\n")
        wr.writerow(faltan)
    
    return dic_nombre_marcas


if __name__ == "__main__":

    path = 'C:\\Users\\masan\\Desktop\\Mario\\ESFM\\Octavo Semestre\\Servicio Social\\Etiquetas'
    dic_nombre_marcas = vectorDatos(path)
    print(len(dic_nombre_marcas))
