import numpy as np
from PIL import Image
import cv2
import torch


def transformacion_datos(data, output_size=150):
    
    path = 'C:\\Users\\masan\\Desktop\\Mario\\ESFM\\Octavo Semestre\\Servicio Social\\imagenes'
    nombre_imagen = data[-1][0]
    puntos = np.array([])
    
    for fila_datos in data[:-1]:
        puntos = np.append(puntos, np.array(fila_datos[5:]))
    puntos = puntos.reshape(14,2)
        
    h, w = 540, 960
    
    if h > w:
        new_h, new_w = output_size * h / w, output_size
    else:
        new_h, new_w = output_size, output_size * w / h
        
    new_h, new_w = int(new_h), int(new_w)
    
    img = Image.open(f'{path}\\{nombre_imagen}')
    img = np.asarray(img)
    img = cv2.resize(img, (new_w, new_h))
    
    # Pasamos a blanco y negro
    image_copy = img.copy()    
    image_copy = cv2.cvtColor(image_copy, cv2.COLOR_RGB2GRAY)
    image_copy=  image_copy/255.0    
    img = image_copy
    
    # escalado de puntos
    puntos = puntos * [new_w/w, new_h/h]
    
    # Pasamos la imagen y los puntos a tensor
    if(len(img.shape) == 2):
        img = img.reshape(img.shape[0], img.shape[1], 1)
        
    img = img.transpose((2, 0, 1))
        
    return {'image': torch.from_numpy(img), 'puntos': torch.from_numpy(puntos)}

if __name__ == '__main__':
    pass