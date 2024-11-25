from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import Select

from dotenv import load_dotenv
load_dotenv()
from os import environ


my_secret_image = environ.get("BANK_SECRET_IMAGE") + environ.get("BANK_SECRET_IMAGE_SECOND_PART")

def start():
 
    driver = webdriver.Chrome()
    driver.get("https://online.bancamiga.com/?p=1")
    
    driver.implicitly_wait(10)
    
    
    
    swal_element = driver.find_element(By.XPATH, "/html/body/div[6]/div/div[10]/button[1]")
    

    if not environ.get("BANK_DNI"):    
        dni = input("Set DNI: ")
        username = input("Set Username: ")
        password = input("Set password: ")
    else:
        dni = environ.get("BANK_DNI")
        username = environ.get("BANK_USERNAME")
        password = environ.get("BANK_PASSWORD")
    
    
    
    d = driver.find_element(By.ID, "documento")
    u = driver.find_element(By.ID, "u")
    p = driver.find_element(By.ID, "p")

    d.send_keys(dni)
    u.send_keys(username)
    p.send_keys(password)
    
    
    swal_element.click()
    
    next_login_step_button = driver.find_element(By.XPATH, '//*[@id="cmdLogin"]')
    next_login_step_button.click()
    # TODO: Validate if the session is active (swal)
    
    google_auth_code = input("Code Of Google Authenticator: ")
    google_auth_code_input = driver.find_element(By.ID, 'code')
    google_auth_code_input.send_keys(google_auth_code)
    
    next_login_step_button = driver.find_element(By.ID, 'cmdLogin')
    next_login_step_button.click()
    sleep(3)
    
    try:
        bank_home(driver)
    except Exception as e:
        logout(driver)
  
    
    
    
    sleep(5)
    # driver.close()
    
def logout(driver: webdriver.Chrome):
    driver.execute_script("arguments[0].click()", driver.find_element(By.XPATH, '//*[@id="logout"]/span/a'))
    swal_confirm(driver)
    driver.close()
    print("Logout successfully")
    
def swal_confirm(driver: webdriver.Chrome):
    driver.find_element(By.XPATH, '/html/body/div[8]/div/div[10]/button[1]').click()

    
def swal_content(driver: webdriver.Chrome):
    text = driver.find_element(By.ID, 'swal2-content')
    print("Swal content -> ",text.text.strip())
    return text.text.strip()

def bank_home(driver: webdriver.Chrome):
    driver.find_element(By.ID, 'cmdOpenPOS').click()
    
    try:
        mesa_cambio_button = driver.find_element(By.ID, 'cmdMesaCambio')
        driver.execute_script("arguments[0].click();", mesa_cambio_button)
        
    except Exception  as e:
        print("This element is not interactable")
        logout(driver)
    
    sleep(3)
    secret_images = driver.find_elements(By.CLASS_NAME, "img-picker")
    for secret_image in secret_images:
        secret_image_src = secret_image.get_attribute("src")
        if(secret_image_src.strip() == my_secret_image.strip()):
            try:
                driver.execute_script("arguments[0].click();", secret_image)

            except Exception  as e:
                print("Secret Image  is not interactable")
                logout(driver)
            sleep(3)
            break
        
    try:
        menudeo_button = driver.find_element(By.ID, "ui-id-2")
        
        menudeo_button.click()
    except Exception  as e:
        print("Menudeo Button is not interactable")
        logout(driver)
    sleep(2)
    
    try:
        menudeo_compra_button = driver.find_element(By.ID, "cmdAddC")
        menudeo_compra_button.click()
    except Exception  as e:
        print("Menudeo Compra Button is not interactable")
        logout(driver)
    
    sleep(2)
    menudeo_desde_select = Select(driver.find_element(By.ID, "desde"))
    menudeo_desde_select.select_by_value(environ.get("BANK_CORRIENTE"))
    sleep(1)
    
    menudeo_hasta_select = Select(driver.find_element(By.ID, "hasta"))
    menudeo_hasta_select.select_by_value(environ.get("BANK_CASH"))
    sleep(1)
    
    Select(driver.find_element(By.ID, "origen")).select_by_value(str(1))
    Select(driver.find_element(By.ID, "destino")).select_by_value(str(5))
    monto = input("Amount To Buy: ")
    driver.find_element(By.ID, "monto").send_keys(str(monto))
    buy(driver)



def buy(driver: webdriver.Chrome, attemps = 0):
    driver.find_element(By.XPATH, '//*[@id="form"]/footer/div[2]/button[1]').click()
    swal_confirm(driver)
    print("Buy confirmed, wait 5 seconds...")
    
    sleep(5)
    
    if swal_content(driver) == "Estimado cliente, en este momento no podemos procesar su operación. Por favor, intente más tarde".strip():
        swal_confirm(driver)
        sleep(2)
        print("Try again... Attemp:", attemps)
        buy(driver, attemps + 1)
    else:
        print("Buy successfully :D")
        logout(driver)
        

if __name__ == "__main__":
    start()
    
    
    
    
    
    
    
    
