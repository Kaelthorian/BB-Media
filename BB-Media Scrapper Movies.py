import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import time
import re


def ScrappingLinks(Link):
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

    print(combined_df)


def ScrappingInfo(Link):
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

    for i in times:
        for li in i.find_all('li'):
            if re.search(r'\b\d+\s*hr\b', li.text) or re.search(r'\b\d+\s*min\b', li.text):
                time = li.text.strip()
                break

    descripcion = [p.text.strip() for p in inf if p.text.strip()]

    data_dict = {
        'Nombre': [nombre],
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
    print(nombre)


def Start():
    start_time = time.time()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'Links', 'LinksPeliculas.csv')

    df = pd.read_csv(csv_path)
    ex_links = df['Row']

    for link in ex_links:
        ScrappingInfo(link)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo de ejecución pelicula: {execution_time:.4f} segundos")


ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6419c584dbdaaa000845cad0?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/631a0596822bbc000747c340?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/604a66306fb8e0000718b7d5?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6245e3e75b72240007129448?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e98badabe135f0007f6fd38?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6245bf61a380fd00075eb902?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e2efdab7606430009a60684?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e664a3d461ef80007c74a4b?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e2f057012f8f9000947823a?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e664ad54d9608000711bf62?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e98ba08d29fad000774d8f1?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e45b93b0226550009f458f0?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e45b6c57cbf380009c9fd3c?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e45bb571dbf7b000935ab55?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/60cb966907f6370007c0e05e?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e664aac9cbc7000077f8ad9?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/60c0cc32c72308000700c61a?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/60cb97ae9f11af0007902c42?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/62473fdd9c333900071c587e?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6539313c67bd1a00084d8023?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6144cbd27bdf170007e1ea12?lang=en')
Start()
