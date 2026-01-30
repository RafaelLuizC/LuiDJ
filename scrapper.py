import requests, json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Configurações do ambiente
driver = webdriver.Firefox()
headers = requests.utils.default_headers()
headers['User-Agent'] = 'Coloque o seu user agent aqui'


def extrair_dados(driver, timeout=10):
    musicas = []

    # Espera até que os elementos de música estejam presentes na página
    # Raspagem desses dados somente para fins educacionais, :D

    # Aguarda os resultados aparecerem
    WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located(
            (By.TAG_NAME, 'ytmusic-responsive-list-item-renderer')
        )
    )

    elementos = driver.find_elements(
        By.TAG_NAME, 'ytmusic-responsive-list-item-renderer'
    )

    for elemento in elementos:
        #Precisa ajustar o título
        titulo = ''
        titulos = elemento.find_elements(By.TAG_NAME, 'yt-formatted-string')
        if titulos:
            titulo = titulos[0].text.strip()

        # Tipo ou Subtítulo
        tipo = ''
        subtitulo = elemento.find_elements(By.CLASS_NAME, 'secondary-flex-columns')
        if subtitulo:
            tipo = subtitulo[0].text.strip()

        # Artista
        artista = 'Desconhecido'
        if '•' in tipo:
            partes = tipo.split('•')
            if len(partes) > 1:
                artista = partes[1].strip()

        # Link
        link = None
        links = elemento.find_elements(By.TAG_NAME, 'a')
        if links:
            link = links[0].get_attribute('href')

        # Se não tiver titulo, ele remove o item.
        # if not titulo:
        #     continue  # ignora itens vazios

        print(f'Título: {titulo} | Artista: {artista}')

        musicas.append({
            'titulo': titulo,
            'artista': artista,
            'tipo': tipo,
            'link': link
        })

    return musicas


def acessar_site(url):
    driver.get(url)

    musicas = extrair_dados(driver)
    print(json.dumps(musicas, indent=4, ensure_ascii=False))

    with open('output.json', 'w+', encoding='utf-8') as f:
        json.dump(musicas, f, ensure_ascii=False, indent=4)

    driver.quit()


string_busca = input("Digite o nome da música ou álbum que deseja buscar: ")

url = f"https://music.youtube.com/search?q={string_busca.replace(' ', '+')}"

acessar_site(url)
