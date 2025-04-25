from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# Configurações do driver principal (para coletar os links da página inicial)

driver = webdriver.Chrome()
driver.get("https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-es?pe=100000&me=10000")

time.sleep(5)  # Espera para garantir o carregamento da página
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

links = soup.find_all('a', class_='olx-adcard__link')
driver.quit()  # Fecha o driver principal

# Processa cada link separadamente com um novo driver
for link in links:
    href = link.get('href')
    print("Anúncio:", link.text.strip(), "-- Link:", href)
    
    if href:
        try:
            # Criar novo driver por link
            driver = webdriver.Chrome()

            driver.get(href)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            valor = driver.find_element(By.XPATH, '//*[@id="price-box-container"]/div[1]/div[1]/span')

            dados = soup.find_all('div', class_='ad__sc-2h9gkk-0 dLQbjb olx-container olx-container--outlined olx-d-flex')

            print(valor.text)
            
            for dado in dados:
                titulo = dado.find('span', class_='olx-text olx-text--overline olx-text--block olx-mb-0-5 olx-color-neutral-120')
                descricao = dado.find('a')

                if titulo:
                    print(titulo.text.strip())

                
                if descricao:
                    print(descricao.text.strip())
                else:
                    descricao = dado.find('span', class_='ad__sc-hj0yqs-0 ekhFnR')
                    print(descricao.text.strip())

            
            #(i) marca, (ii) modelo, (iii) ano, (iv) cambioAutomatico, (v) se é sedan ou hatch, (vi) cor, (vii) valor e (viii) municipio

        except Exception as e:
            print("Erro ao acessar:", href)
            print("Detalhes:", str(e))

        finally:
            driver.quit()
            #teste