# scraper.py
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd


def get_url(searchTerm):
    searchTerm = searchTerm.replace(' ', '+')
    url = f"https://www.etsy.com/search?q={searchTerm}&ref=search_bar"
    return url


def get_products(card):
    try:
        name_of_item = card.find('h3').text.strip()
    except:
        name_of_item = ''

    try:
        price = card.find('span', {'class': 'currency-value'}).text.strip()
    except:
        price = ''

    try:
        download = card.find('p', {'class': 'wt-text-body-smaller'}
                             ).text.strip().replace('(', '').replace(')', '').replace('-', '')
        if 'k' in download:
            number_of_download = float(download.replace('k', '')) * 1000
        else:
            number_of_download = float(download)
    except:
        number_of_download = ''

    try:
        item_url = card.find('a').get('href')
    except:
        item_url = ''

    products_info = (name_of_item, price, number_of_download, item_url)
    return products_info


def scrape_etsy(search_term):
    url = get_url(search_term)

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    cards = soup.find_all('div', {'class': 'search-listing-card--desktop'})

    record_products = []

    for card in cards:
        product_details = get_products(card)
        record_products.append(product_details)

    filename = f'{search_term}.csv'
    csv_filename = filename.replace(' ', '_')
    filepath = f'./results/{csv_filename}'

    col = ['name of item', 'price (RM)', 'number of downloads', 'item URL']
    product_data = pd.DataFrame(record_products, columns=col)
    product_data.to_csv(filepath)

    print("Data has been saved to:", filepath)

    time.sleep(2)
    driver.quit()

    return filepath


if __name__ == "__main__":
    search_term = input("Enter your search product: ")
    scrape_etsy(search_term)
