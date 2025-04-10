from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

chromedriver_path = "chromedriver.exe"  
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

csv_file = r"C:/Users/Pongo/Desktop/Big Data/cryptodata.csv"
url = "https://coinmarketcap.com/"  
driver.get(url)

time.sleep(5)

def fetch_data():
    
    coin_names = driver.find_elements(By.CSS_SELECTOR, ".sc-65e7f566-0.iPbTJf.coin-item-name")
    coin_prices = driver.find_elements(By.CSS_SELECTOR, ".sc-142c02c-0.lmjbLF")
    coin_growth_1h = driver.find_elements(By.CSS_SELECTOR, ".sc-1e8091e1-0.jgYsZM")
    coin_growth_24h = driver.find_elements(By.CSS_SELECTOR, ".sc-1e8091e1-0.fDGzbr")
    coin_volume = driver.find_elements(By.CSS_SELECTOR, ".sc-4c05d6ef-0.sc-cb798334-0.dlQYLv.jltLyq")

    data = []
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    count = min(len(coin_names), len(coin_prices), len(coin_growth_1h), len(coin_growth_24h), len(coin_volume))

    print(f"Total Coins: {count}")

    for i in range(count):
        name = coin_names[i].text.strip()
        raw_price = coin_prices[i].text.strip() 
        price = raw_price if raw_price != "" else "0%"
        raw_growth_1h = coin_growth_1h[i].text.strip()
        growth_1h = raw_growth_1h if raw_growth_1h != "" else "0%"
        raw_growth_24h = coin_growth_24h[i].text.strip()
        growth_24h = raw_growth_24h if raw_growth_24h != "" else "0%"
        raw_volume = coin_volume[i].text.strip() 
        volume = raw_volume if raw_volume != "" else "0"
        
        data.append([timestamp, name, price, growth_1h, growth_24h, volume])
        print(f"Time: {timestamp} - {name} - {price} - (1H) {growth_1h} - (24H) {growth_24h} - {volume}")
    
    return data

print("Scraping Data...")
num_pages = 6
        
try:
    while True:
        total_data = []

        for page in range(1, num_pages + 1): # looping cek semua page
            url = f"https://coinmarketcap.com/?page={page}"
            driver.get(url)
            # Give the page enough time to load
            time.sleep(10)
            page_data = fetch_data()      
            total_data.extend(page_data)

        if total_data: #ada value
            df = pd.DataFrame(total_data, columns=["Date", "Coin Name", "Price", "1h Growth", "24h Growth", "Volume"])
            df.to_csv(csv_file, mode='a', index=False, encoding="utf-8", header=not os.path.exists(csv_file))
            print("Data saved to cryptodata.csv\n\n")
        time.sleep(5)
except KeyboardInterrupt:
    print("Scraping Terminated..")
finally:
    driver.quit()
