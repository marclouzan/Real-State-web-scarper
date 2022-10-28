#Hi there!
#This is an exemple using a Chrome webdriver 
#I did this because of a friend that works in Real State, he demanded me a program that returns a report of determinated spanish costs properties, in this case, to rent.
#Rentalia.com was not one of the simplest neither the more complex to scrape data so, i think it could be a good example.
#So, we start setting the browser and some specifications options, then create the driver with two arguments: exacutable driver path  and the options.
#Then declaring the main url and setting it at the driver momentarily and start driving to the elements we want.



from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv
from selenium.webdriver.common.by import By
#import pandas as pd
#import numpy as np
#from email import header

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

#Accept cookies button
cookies = driver.find_element(By.XPATH, '//*[@id="didomi-host"]/div/div/div/div//div[2]/button[2]')
cookies.click()

#Locations desired
locations = ["Costa Brava", "Alicante", "Barcelona", "Madrid", "Castelldefels", "Gavà"]  


#This render is important, allow us to scroll up and down to have access to al elements in the pages, 
# if we not define a render, our program only can extract data of the principal few elements 'he' sees at the screen and not all the content.

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
    
    
    search_btn = driver.find_element(By.XPATH , '//*[@id="masterContainer"]/div/div[1]/div/form/div/div[5]/button')
    search_btn.click()
    
    print(f"reached page {url}")   
    
    #First row of the document
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
                
                
                #In this case, to extract the phone number we have to move the driver again so we set the link we recently declared
                # and go to the particular property link.
                driver.get(link)
                render()
                
                try:
                    capacity = driver.find_element(By.CLASS_NAME, 'characteristic').find_element(By.TAG_NAME, 'p').text
                    print(capacity)
                except:
                    capacity = ''
            
                
                #This is the mainly field that we want
                try:
                    tel = driver.find_element(By.CLASS_NAME, 'owner').find_element(By.CLASS_NAME, 'editButtons').find_elements(By.TAG_NAME, 'a')[0].text.split(" ")[1]
                    print(tel)
                except:
                    tel = ''    
                
                
                line = [portal, type, title, lctn, link, price, capacity, tel]
                
                #Getting out to return to property list page
                back_menu = driver.find_element(By.CLASS_NAME, 'navigation').find_element(By.TAG_NAME, 'a')
                back_menu.click()
                render()
                
                #Adding property announcement 
                wr.writerow(line)
               
            
            #Selecting next page button 
            nextpage = driver.find_element(By.XPATH, '//*[@id="masterContainer"]/div/div[3]/div[2]/ul/li[last()]/a').get_attribute('href')
            driver.get(nextpage)  
            
            