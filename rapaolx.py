import selenium
from bs4 import BeautifulSoup

from selenium import webdriver

driver = webdriver.Edge()
driver.get("https://es.olx.com.br/norte-do-espirito-santo/autos-e-pecas/carros-vans-e-utilitarios/saveiro-robust-1-6-cs-2022-12-000km-1392640812?lis=listing_2020")

html = driver.page_source

driver.close()

soup = BeautifulSoup(html, 'html.parser')

dados = soup.find_all('a', class_='olx-link olx-link--small olx-link--grey ad__sc-2h9gkk-3 lkkHCr')

for dado in dados:
    print(dado.text)