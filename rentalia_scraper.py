from email import header
from requests import head
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np


options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument("user-data-dir=selenium")
options.add_argument("--remote-debugging-port=9222")
options.add_argument('--disable-dev-shm-usage')

url = "https://es.rentalia.com/" 
driver = webdriver.Chrome(executable_path = r"C:\Users\marcl\chromedriver_106\chromedriver.exe", options = options)

driver.implicitly_wait(15)
driver.get(url) 

cookies = driver.find_element(By.XPATH, '//*[@id="didomi-host"]/div/div/div/div//div[2]/button[2]')
cookies.click()

locations = ["Costa Brava", "Alicante", "Barcelona", "Madrid", "Castelldefels", "Gavà"]  

def render():
    for i in range(1,22):
        ActionChains(driver).send_keys(Keys.SPACE).perform()
    for i in range(1,192):
        ActionChains(driver).send_keys(Keys.UP).perform()

for loc in locations:
    try:
        input_field = driver.find_element(By.CLASS_NAME, 'locationInput ng-pristine ng-valid ng-scope ng-isolate-scope ng-empty ng-touched')   
    except:    
        input_field = driver.find_element(By.XPATH, '//*[@id="masterContainer"]/div/div[1]/div/form/div/div[1]/span/input')
    
    
    input_field.send_keys(loc)
    ActionChains(driver).send_keys(Keys.DOWN).send_keys(Keys.ENTER).perform()
    time.sleep(3)
    
    try:
        f = driver.find_element(By.XPATH , '//*[@id="masterContainer"]/div/div[1]/div/form/div/div[5]/button')
        print(f)
        a = ActionChains(driver)
        h = a.move_to_element(f)
        h.perform()
        h.send_keys(Keys.ENTER).perform()
    except:  
        f = ''    
    
    
    print(f"reached page {url}")   
    
    headers = ['Portal', 'Tipo','Título','Ubicación', 'Link', 'Precio por noche', 'Capacidad','Teléfono móvil']
    with open('rentalia.csv','w+', encoding = 'utf-8', newline='') as f:
        wr = csv.writer(f, dialect = 'excel')
        wr.writerow(headers)
        
        while(True):
         
    
            render()

            props = driver.find_elements(By.CLASS_NAME, 'itemContent')
            
            for a in range(0,len(props)):  
                
                prop = driver.find_elements(By.CLASS_NAME, 'itemContent')[a] 
                
                portal = 'Rentalia'
                type = 'Alquiler'
                
                try:
                    title = prop.find_element(By.CLASS_NAME, 'title').find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME, 'h3').text
                    print("title",title)
                   
                except:  
                    title = ''    
                

                try:  
                    lctn = prop.find_element(By.CLASS_NAME, 'title').find_element(By.TAG_NAME,'a').find_element(By.TAG_NAME, 'h4').text
                    print(lctn)
                except:
                    lctn = ""    

                try:
                    link = prop.find_element(By.CLASS_NAME, 'title').find_element(By.TAG_NAME, 'a').get_attribute('href')
                    print(link)
                except:  
                    link = ''   

                try:
                    price = prop.find_element(By.CLASS_NAME, 'price').find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'span').text.split(' p')[0]
                    print(price)
                except:  
                    price = ''    
                
                line = [portal, type, title, lctn, link, price]
                
                driver.get(link)
                render()
                
                try:
                    capacity = driver.find_element(By.CLASS_NAME, 'characteristic').find_element(By.TAG_NAME, 'p').text
                    print(capacity)
                except:
                    capacity = ''
                    
                line.append(capacity)
                
                try:
                    tel = driver.find_element(By.CLASS_NAME, 'owner').find_element(By.CLASS_NAME, 'editButtons').find_elements(By.TAG_NAME, 'a')[0].text.split(" ")[1]
                    print(tel)
                except:
                    tel = ''    

                line.append(tel)
                
                back_menu = driver.find_element(By.CLASS_NAME, 'navigation').find_element(By.TAG_NAME, 'a')
                back_menu.click()
                render()
                
                wr.writerow(line)
               
            
            
            nextpage = driver.find_element(By.XPATH, '//*[@id="masterContainer"]/div/div[3]/div[2]/ul/li[last()]/a').get_attribute('href')
            driver.get(nextpage)  
            
            