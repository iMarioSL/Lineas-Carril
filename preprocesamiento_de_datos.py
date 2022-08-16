import torchvision.transforms as transforms
import PIL

def vectorImagenes(nombre_imagenes, path):
    """_summary_

    Args:
        imagenes (Array): Array de nombre de las imagenes
        path (Strig): La ruta de las imagenes
        dict = {'nombre_imagen': [vectorDeDatos]}
    """
    
    dic_nombre_imagen = {}
    transform_to_tensor = transforms.Compose([transforms.ToTensor()])

    for nombre_imagen in nombre_imagenes:
        imagen_individual = PIL.Image.open(f"{path}\\{nombre_imagen}")
        imagen_tensor = transform_to_tensor(imagen_individual)
        dic_nombre_imagen[nombre_imagen] = imagen_tensor
    
    return dic_nombre_imagen

if __name__ == '__main__':
    
    dic_nombre_imagen = vectorImagenes(imagenes)