import re
import base64
from io import BytesIO
import requests
from PIL import Image  



#lee el archivo html
with open('./Animales-practica/texto.html', 'r', encoding='utf-8') as archivo:
    contenido = archivo.read()


#busca el patron <img src=
patron = r'<img src="([^"]+)"'
resultados = re.findall(patron, contenido)


#para cada uno de los elementos del patron encontrados
contador=0
with open("./Animales-practica/resultado.txt", 'a') as archivo:
    for resultado in resultados:

        #por un lado, si esta cadena (data:image...) no esta en el elemento encontrado, se descarga de una forma
        if "data:image/png;base64" not in resultado:
                
                #quitamos cabecera
                posicion = resultado.find(",")
                if(posicion==22):
                    if(contador<151):
                            cortado=resultado[23:]
                            contador=contador+1
                            archivo.write(cortado + '\n\n\n\n\n')

                            #descargamos imagen
                            imagen_decodificada = base64.b64decode(cortado)
                            stream = BytesIO(imagen_decodificada)
                            imagen = Image.open(stream)
                            imagen.save("./Animales-practica/fotos/periquito/periquito"+str(contador)+".jpg")
                            print("Imagen descargada exitosamente.")

        #por otro lado si en el elemento se encuentra esta cadena ("encrypte..."), se descarga de otra forma
        if "encrypted-tbn0" in resultado:
                response = requests.get(resultado)
                contador=contador+1

                if(contador<151):

                    #descargamos imagen
                    if response.status_code == 200:
                        with open("./Animales-practica/fotos/periquito/periquito"+str(contador)+".jpg", "wb") as f:
                            f.write(response.content)
                        print("Imagen descargada exitosamente.")
                    else:
                        print(f"Error al descargar la imagen. Código de estado: {response.status_code}")

print(contador)     

