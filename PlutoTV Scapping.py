from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import time
import re

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)


def StartTV():
    start_time = time.time()
    driver.get("https://pluto.tv/latam/live-tv")
    current_url = driver.current_url
    html_page = requests.get(current_url).text
    data = BeautifulSoup(html_page, 'html.parser')
    span = data.find_all('span')
    canal = []

    for i in span:
        titu = i.text.strip()
        if '@' in titu:
            continue
        if '©' in titu:
            continue
        canal.append(titu)

    new_data_dict = {'Canal': canal}
    new_df = pd.DataFrame(new_data_dict)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'DataBase', 'TV.csv')

    if os.path.isfile(csv_path):
        existing_df = pd.read_csv(csv_path)
        combined_df = pd.concat([existing_df, new_df])
        combined_df.drop_duplicates(subset=['Canal'], inplace=True)
    else:
        combined_df = new_df
    combined_df.to_csv(csv_path, mode='w', index=False)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo de ejecución TV Live: {execution_time:.4f} segundos")

def ScrappingLinksMovies(Link):
    HTML = f"{Link}"
    html_page = requests.get(HTML).text
    data = BeautifulSoup(html_page, 'html.parser')
    soup = data.find_all('a', type="button", class_='')
    rows = []
    for i in soup:
        href = i.get('href')
        if href.find("movies") != -1:
            rows.append(href)

    new_data_dict = {'Row': rows}
    new_df = pd.DataFrame(new_data_dict)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'Links', 'LinksPeliculas.csv')

    if os.path.isfile(csv_path):
        existing_df = pd.read_csv(csv_path)
        combined_df = pd.concat([existing_df, new_df])
        combined_df.drop_duplicates(subset=['Row'], inplace=True)
    else:
        combined_df = new_df
    combined_df.to_csv(csv_path, mode='w', index=False)


def ScrappingInfoMovies(Link):
    HTML = f"https://pluto.tv{Link}"
    html_page = requests.get(HTML).text
    data = BeautifulSoup(html_page, 'html.parser')
    title = data.find('h1')
    inf = data.find_all('p')
    times = data.find_all('ul')

    descripcion = []
    nombre = title.text.strip() if title else "N/A"
    link = HTML
    time = "N/A"
    rate = "N/A"
    gen = "N/A"

    for i in times:
        for li in i.find_all('li'):
            if re.search(r'^PG$', li.text) or re.search(r'^R$', li.text) or re.search(r'^TV-G$', li.text) or re.search(r'^NC-17$', li.text) or re.search(r'^Y$', li.text) or re.search(r'^TV-14$', li.text) or re.search(r'^MA$', li.text) or re.search(r'^Y7$', li.text) or re.search(r'^PG-13$', li.text) or re.search(r'^TV-MA$', li.text) or re.search(r'^TV-PG$', li.text):
                rate = li.text.strip()
                if rate == "":
                    rate = "N/A"
            if re.search(r'^Comedy$', li.text) or re.search(r'^Horror$', li.text) or re.search(r'^Drama$', li.text) or re.search(r'^War$', li.text) or re.search(r'^Action & Adventure$', li.text) or re.search(r'^Family$', li.text) or re.search(r'^Thriller$', li.text) or re.search(r'^Sci-Fi$', li.text) or re.search(r'^Adventure$', li.text) or re.search(r'^Documentary$', li.text) or re.search(r'^Romance$', li.text) or re.search(r'^Accion$', li.text) or re.search(r'^Fantasy$', li.text) or re.search(r'^Sci-Fi & Fantasy$', li.text) or re.search(r'^Crime$', li.text) or re.search(r'^Western$', li.text) or re.search(r'^Anime$', li.text) or re.search(r'^Young Adult$', li.text) or re.search(r'^Faith & Spirituality$', li.text) or re.search(r'^Gay$', li.text) or re.search(r'^Independent$', li.text) or re.search(r'^Entertainment$', li.text) or re.search(r'^Musical$', li.text) or re.search(r'^Other$', li.text) or re.search(r'^Thrillers$', li.text):
                gen = li.text.strip()
                if gen == "":
                    gen = "N/A"

    descripcion = [p.text.strip() for p in inf if p.text.strip()]

    data_dict = {
        'Nombre': [nombre],
        'Categoria': [rate],
        'Genero': [gen],
        'Duracion': [time],
        'Link': [link],
        'Descripcion': [', '.join(descripcion)]
    }
    df_new = pd.DataFrame(data_dict)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'DataBase', 'Peliculas.csv')

    if os.path.isfile(csv_path):
        df_existing = pd.read_csv(csv_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.drop_duplicates(subset=['Link'], inplace=True)
    else:
        df_combined = df_new

    df_combined.to_csv(csv_path, mode='w', index=False)


def StartMovies():
    start_time = time.time()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'Links', 'LinksPeliculas.csv')

    df = pd.read_csv(csv_path)
    ex_links = df['Row']

    for link in ex_links:
        ScrappingInfoMovies(link)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo de ejecución pelicula: {execution_time:.4f} segundos")

def StartLinksFetchMovies():
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6419c584dbdaaa000845cad0?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/631a0596822bbc000747c340?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/604a66306fb8e0000718b7d5?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6245e3e75b72240007129448?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e98badabe135f0007f6fd38?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6245bf61a380fd00075eb902?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e2efdab7606430009a60684?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e664a3d461ef80007c74a4b?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e2f057012f8f9000947823a?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e664ad54d9608000711bf62?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e98ba08d29fad000774d8f1?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e45b93b0226550009f458f0?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e45b6c57cbf380009c9fd3c?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e45bb571dbf7b000935ab55?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/60cb966907f6370007c0e05e?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e664aac9cbc7000077f8ad9?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/60c0cc32c72308000700c61a?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/60cb97ae9f11af0007902c42?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/62473fdd9c333900071c587e?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6539313c67bd1a00084d8023?lang=en')
    ScrappingLinksMovies(
        'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6144cbd27bdf170007e1ea12?lang=en')



def ScrappingLinksSeries(Link):
    HTML = f"{Link}"
    html_page = requests.get(HTML).text
    data = BeautifulSoup(html_page, 'html.parser')
    soup = data.find_all('a', type="button", class_='')
    rows = []
    for div in soup:
        href = div.get('href')
        if href.find("series") != -1:
            rows.append(href)

    data_dict = {'Row': rows}
    new_df = pd.DataFrame(data_dict)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'Links', 'LinksSeries.csv')

    if os.path.isfile(csv_path):
        existing_df = pd.read_csv(csv_path)
        combined_df = pd.concat([existing_df, new_df])
        combined_df.drop_duplicates(subset=['Row'], inplace=True)
    else:
        combined_df = new_df
    combined_df.to_csv(csv_path, mode='w', index=False)



def ScrappingInfoSeries(Link):
    HTML = f"https://pluto.tv{Link}"
    html_page = requests.get(HTML).text
    data = BeautifulSoup(html_page, 'html.parser')
    title = data.find('h1')
    inf = data.find_all('p')

    descripcion = [p.text.strip() for p in inf if p.text.strip()]
    nombre = title.text.strip() if title else "N/A"
    link = HTML

    data_dict = {'Nombre': nombre, 'Link': link, 'Descripcion': descripcion}
    df = pd.DataFrame(data_dict)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'DataBase', 'Series.csv')

    file_exists = os.path.isfile(csv_path)
    df.to_csv(csv_path, mode='a', index=False, header=not file_exists)



def StartSeries():
    start_time = time.time()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'Links', 'LinksSeries.csv')

    df = pd.read_csv(csv_path)
    ex_links = df['Row']

    for link in ex_links:
        ScrappingInfoSeries(link)

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Tiempo de ejecución series: {execution_time:.4f} segundos")

def StartLinksFetchSeries():
    ScrappingLinksSeries(
        'https://pluto.tv/latam/on-demand/619043246d03190008131b89/6245c1e23ca9b400078727bc?lang=en')
    ScrappingLinksSeries(
        'https://pluto.tv/latam/on-demand/619043246d03190008131b89/62473ee1a8099000076c0783?lang=en')
    ScrappingLinksSeries(
        'https://pluto.tv/latam/on-demand/619043246d03190008131b89/625db92c5c4b590007b808c6?lang=en')
    ScrappingLinksSeries(
        'https://pluto.tv/latam/on-demand/619043246d03190008131b89/63dd2358a8b22700082367ff?lang=en')
    ScrappingLinksSeries(
        'https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941e09db549e0007ef2dc9?lang=en')
    ScrappingLinksSeries(
        'https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941dfa8ab0970007f41c59?lang=en')
    ScrappingLinksSeries(
        'https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941de9e03c74000701ed4f?lang=en')
    ScrappingLinksSeries(
        'https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941dc7fd0bc30007db1b6d?lang=en')
    ScrappingLinksSeries(
        'https://pluto.tv/latam/on-demand/619043246d03190008131b89/5e2f061eeb7c04000967bf70?lang=en')
    ScrappingLinksSeries(
        'https://pluto.tv/latam/on-demand/619043246d03190008131b89/5e45bbf395fb000009945cf0?lang=en')
    ScrappingLinksSeries(
        'https://pluto.tv/latam/on-demand/619043246d03190008131b89/5f908026a44d9c00081fd41d?lang=en')
    
    
    
start_time_Scrap = time.time()
print("Buscando links...")
StartLinksFetchMovies()
StartLinksFetchSeries()

print("Scrapping TV Live (Tiempo promedio de espera: 6 segundos)")
StartTV()
print("Scrapping Series (Tiempo promedio de espera: 175 segundos)")
StartSeries()
print("Scrapping Peliculas (Tiempo promedio de espera: 1800 segundos)")
StartMovies()

end_time_Scrap = time.time()
execution_time_Scrap = end_time_Scrap - start_time_Scrap
print(f"Tiempo de ejecución total: {execution_time_Scrap:.4f} segundos")