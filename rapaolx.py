from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver

def capturarAnuncio():
    anuncios = []

    # Configurações do driver principal (para coletar os links da página inicial)
    driver = webdriver.Chrome()
    driver.get("https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-es?pe=100000&me=10000")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) # Espera para garantir o carregamento da página com base na tag body
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.find_all('a', class_='olx-adcard__link')
    driver.quit()  # Fecha o driver principal

    # Processa cada link separadamente com um novo driver
    for i, link in enumerate(links): #limitar a 10 anuncios // fazer o vídeo de comprovação de execução com até 3 anuncios
        if i >= 3:
            break
        
        href = link.get('href')
        #print("Anúncio:", link.text.strip(), "-- Link:", href)
        
        if href:
            try:
                # Criar novo driver por link
                driver = webdriver.Chrome()
                driver.get(href)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) # Espera para garantir o carregamento da página com base na tag body

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                anuncio = {
                    'marca': None,
                    'modelo': None,
                    'ano': None,
                    'cambio': None,
                    'tipo': None, 
                    'cor': None,
                    'valor': None,
                    'municipio': None
                }

                valor = driver.find_element(By.XPATH, '//*[@id="price-box-container"]/div[1]/div[1]/span') # Captura o valor              
                municipio = soup.find('span', class_='olx-text olx-text--body-small olx-text--block olx-text--semibold olx-color-neutral-110') # Captura o municipio

                dados = soup.find_all('div', class_='ad__sc-2h9gkk-0 dLQbjb olx-container olx-container--outlined olx-d-flex') # Captura as outras informações gerais
                
                if municipio:
                    municipio_limpo = municipio.text.strip().split(',')[0]
                    anuncio['municipio'] = municipio_limpo.strip()

                if valor:
                    valor_limpo = valor.text.strip().split('$')[1]
                    anuncio['valor'] = valor_limpo.strip()

                for dado in dados: # Percorre as caracteristicas gerais de cada anuncio

                    titulo = dado.find('span', class_='olx-text olx-text--overline olx-text--block olx-mb-0-5 olx-color-neutral-120')
                    descricao = dado.find('a')

                    if titulo:
                        titulo_text = titulo.text.strip()
                    
                    if descricao:
                        descricao_text = descricao.text.strip()
                    else:
                        descricao = dado.find('span', class_='ad__sc-hj0yqs-0 ekhFnR')
                        descricao_text = descricao.text.strip()
                
                    if titulo_text == "Marca":
                        anuncio['marca'] = descricao_text
                    
                    if titulo_text == "Modelo":
                        anuncio['modelo'] = descricao_text

                    if titulo_text == "Ano":
                        anuncio['ano'] = descricao_text

                    if titulo_text == "Câmbio":
                        anuncio['cambio'] = descricao_text

                    if titulo_text == "Tipo de veículo":
                        anuncio['tipo'] = descricao_text

                    if titulo_text == "Cor":
                        anuncio['cor'] = descricao_text                    
                    
                anuncios.append(anuncio)

            except Exception as e:
                print("Erro ao acessar:", href)
                print("Detalhes:", str(e))
                print("Tipo do erro:", type(e))

            finally:
                driver.quit()

    return anuncios

anuncios = capturarAnuncio()
print(anuncios)