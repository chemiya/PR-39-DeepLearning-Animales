from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
import requests

#chromedriver para scrapear
url = "https://www.google.com/search?q=periquito&tbm=isch&ved=2ahUKEwj0146ToLSDAxXPmicCHSm1CwwQ2-cCegQIABAA&oq=periquito&gs_lcp=CgNpbWcQAzIECCMQJzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzIKCAAQgAQQigUQQzoFCAAQgAQ6CAgAEIAEELEDOhAIABCABBCKBRBDELEDEIMBOg0IABCABBCKBRBDELEDUPoJWKgTYPgVaABwAHgAgAGrAYgBwQmSAQQwLjEwmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=aIaOZfSDDc-1nsEPqequYA&bih=607&biw=1366&rlz=1C1RXQR_esES1013ES1013"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(3)


#desplazamos hacia abajo para que cargue mas imagenes
for _ in range(3):  
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)


#obtenemos todas las miniaturas de las imagenes
imagenes=driver.find_elements(By.CSS_SELECTOR,".rg_i.Q4LuWd")
time.sleep(3)


#para cada imagen
contador=0
for imagen in imagenes:
    if(contador==50):
        break

    #hacemos click en ella. Se incluye try para si surge alguna excepcion
    try:
        imagen.click()
        time.sleep(3)

        #buscamos el elemento de la imagen grande
        try:
            imagenGrande=driver.find_element(By.XPATH,"/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]")
            src_atributo = imagenGrande.get_attribute("src")
            if("base64" in src_atributo):
                imagenGrande=driver.find_element(By.XPATH,"/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[2]")
                src_atributo = imagenGrande.get_attribute("src")


            #descargamos la imagen
            print(src_atributo)
            if("base64" not in src_atributo):
                try:
                    response = requests.get(src_atributo)
                    if response.status_code == 200:
                        with open("./Animales-practica/fotos/periquito/periquito_"+str(contador)+".jpg", "wb") as f:
                            f.write(response.content)
                        print("Imagen descargada exitosamente.")
                        contador=contador+1
                    else:
                        print(f"Error al descargar la imagen. Código de estado: {response.status_code}")
                except Exception as e:
                    print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")



driver.quit()




