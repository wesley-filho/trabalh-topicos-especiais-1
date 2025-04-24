from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-es?pe=100000&me=10000")

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')
links = soup.find_all('a', class_='olx-adcard__link')  # Encontrar as tags 'a' 

for link in links:
    href = link.get('href')
    print("Anuncio: " + link.text, "-- Link: " + href)
    time.sleep(3)
    if href:
        driver.get(href)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        dados = soup.find_all('div', class_='ad__sc-2h9gkk-0 dLQbjb olx-container olx-container--outlined olx-d-flex')
        
        for dado in dados:
            print(dado.text)


driver.close()