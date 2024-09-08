from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)


def Scrapping():
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


Scrapping()
