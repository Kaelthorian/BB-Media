import requests
import pandas as pd
from bs4 import BeautifulSoup
import os


def ScrappingLinks(Link):
    HTML = f"{Link}"
    html_page = requests.get(HTML).text
    data = BeautifulSoup(html_page, 'html.parser')
    soup = data.find_all('a', type="button", class_='')
    rows = []
    for div in soup:
        href = div.get('href')
        if href.find("movies") != -1:
            rows.append(href)

    data_dict = {'Row': rows}
    df = pd.DataFrame(data_dict)

    csv_path = 'C:/VS-Code/BB-Media/EXLinksMovies.csv'
    file_exists = os.path.isfile(csv_path)
    df.to_csv(csv_path, mode='a', index=False, header=not file_exists)

    print(df)


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

    csv_path = 'C:/VS-Code/BB-Media/Movies.csv'
    file_exists = os.path.isfile(csv_path)
    df.to_csv(csv_path, mode='a', index=False, header=not file_exists)

    print(df)


def Start():
    csv_path = 'C:/VS-Code/BB-Media/EXLinksMovies.csv'
    df = pd.read_csv(csv_path)
    ex_links = df['Row']

    for link in ex_links:
        ScrappingInfo(link)


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
