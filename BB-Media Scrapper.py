import requests
import pandas as pd
from bs4 import BeautifulSoup


def ScrappingLinks():
    HTML = "https://pluto.tv/latam/on-demand/619043246d03190008131b89/6245c1e23ca9b400078727bc"
    html_page = requests.get(HTML).text
    data = BeautifulSoup(html_page, 'html.parser')
    soup = data.find_all('a', type="button", class_='')
    rows = []
    for div in soup:
        href = div.get('href')
        if href.find("series") != -1:
            rows.append(href)

    data_dict = {'Row': rows}
    df = pd.DataFrame(data_dict)

    csv_path = 'c:/VS-Code/BB-Media/EX_links.csv'
    df.to_csv(csv_path, index=False)

    print(df)


def ScrappingInfo(Link):
    HTML = f"https://pluto.tv{Link}"
    html_page = requests.get(HTML).text
    data = BeautifulSoup(html_page, 'html.parser')
    title = data.find('h1')
    inf = data.find_all('p')

    descripcion = []
    nombre = []

    for i in title:
        titu = i.text.strip('h1')
        if titu:
            nombre.append(titu)
    for i in inf:
        desc = i.text.strip('p')
        if desc:
            descripcion.append(desc)

    data_dict = {'Nombre': nombre, 'Descripcion': descripcion}
    df = pd.DataFrame(data_dict)

    csv_path = 'c:/VS-Code/BB-Media/Series.csv'
    df.to_csv(csv_path, index=False)

    print(df)


def Start():
    csv_path = 'c:/VS-Code/BB-Media/EX_links.csv'
    df = pd.read_csv(csv_path)
    ex_links = df['EX Links']

    rows = []
    for link in ex_links:
        ScrappingInfo(link)
