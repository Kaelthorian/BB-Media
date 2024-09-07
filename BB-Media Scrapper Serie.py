import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import time


def ScrappingLinks(Link):
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

    csv_path = 'C:/VS-Code/BB-Media/EXLinksSeries.csv'
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

    descripcion = []
    nombre = []
    link = HTML

    for i in title:
        titu = i.text.strip('h1')
        if titu:
            nombre.append(titu)
    for i in inf:
        desc = i.text.strip('p')
        if desc:
            descripcion.append(desc)

    data_dict = {'Nombre': nombre, 'Link': link, 'Descripcion': descripcion}
    df = pd.DataFrame(data_dict)

    csv_path = 'C:/VS-Code/BB-Media/Series.csv'
    file_exists = os.path.isfile(csv_path)
    df.to_csv(csv_path, mode='a', index=False, header=not file_exists)

    print(nombre)


def Start():
    start_time = time.time()
    csv_path = 'C:/VS-Code/BB-Media/EXLinksSeries.csv'
    df = pd.read_csv(csv_path)
    ex_links = df['Row']

    for link in ex_links:
        ScrappingInfo(link)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo de ejecución series: {execution_time:.4f} segundos")


ScrappingLinks(
    'https://pluto.tv/latam/on-demand/619043246d03190008131b89/6245c1e23ca9b400078727bc?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/619043246d03190008131b89/62473ee1a8099000076c0783?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/619043246d03190008131b89/625db92c5c4b590007b808c6?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/619043246d03190008131b89/63dd2358a8b22700082367ff?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941e09db549e0007ef2dc9?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941dfa8ab0970007f41c59?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941de9e03c74000701ed4f?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941dc7fd0bc30007db1b6d?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/619043246d03190008131b89/5e2f061eeb7c04000967bf70?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/619043246d03190008131b89/5e45bbf395fb000009945cf0?lang=en')
ScrappingLinks(
    'https://pluto.tv/latam/on-demand/619043246d03190008131b89/5f908026a44d9c00081fd41d?lang=en')
Start()
