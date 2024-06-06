import time
import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

#procuring the required links (plots in : Hyderabad, Jaipur, Vishakahapatnam, Chandigarh, Rajkot, Surat, Madurai, Trivandrum, Indore, and Lucknow)
urls = [
    'https://www.99acres.com/search/property/buy/hyderabad?city=269&keyword=Hyderabad&preference=S&area_unit=1&res_com=R',
    'https://www.99acres.com/search/property/buy/jaipur?city=177&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N',
    'https://www.99acres.com/search/property/buy/visakhapatnam?city=62&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N',
    'https://www.99acres.com/search/property/buy/chandigarh?city=73&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N',
    'https://www.99acres.com/search/property/buy/rajkot?city=94&keyword=Rajkot&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N',
    'https://www.99acres.com/search/property/buy/surat?city=95&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N',
    'https://www.99acres.com/search/property/buy/madurai?city=188&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N',
    'https://www.99acres.com/search/property/buy/trivandrum?city=138&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N',
    'https://www.99acres.com/search/property/buy/indore?city=142&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N',
    'https://www.99acres.com/search/property/buy/lucknow?city=205&keyword=Lucknow&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N'
]

# Lists to store the scraped data
Location_Bldng_name = []
Rent = []
Area = []

#dataframe to finally hold the scraped data
df = pd.DataFrame()

# Loop through the each url
for url in urls:
    #connecting system to Chrome through chromedriver
    driver = webdriver.Chrome()
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content,'html.parser')
    wait = WebDriverWait(driver, 20)
    
    # Find all property listings
    results = soup.findAll('div',attrs={'class': 'tupleNew__tupleWrap tupleNew__PremH'})

    # Extract data from each listing
    for row in results:

        #Location
        try:
            location = row.find('h2', attrs={'class': 'tupleNew__propType'}).get_text(strip=True)
            print(f"Location: {location}")
            Location_Bldng_name.append(location)
        except AttributeError:
            Location_Bldng_name.append(None)
        

        #Rent
        try:
            rent_text = row.find('div', attrs={'class': 'tupleNew__priceValWrap'}).get_text(strip=True)
            # Remove rupee symbol (₹)
            rent = rent_text.replace('₹', '').strip()
            print(f"Price: {rent}")
            Rent.append(rent)  
        except AttributeError:
            Rent.append(None)
     
        #Area
        try:
            area = row.find('div', attrs={'class': 'tupleNew__totolAreaWrap'}).get_text(strip=True)
            print(f"Area: {area}")
            Area.append(area)
        except AttributeError:
            Area.append(None)

  
        # Making lists of same length
        max_length = max(len(Location_Bldng_name), len(Rent), len(Area))
        Location_Bldng_name.extend([None] * (max_length - len(Location_Bldng_name)))
        Rent.extend([None] * (max_length - len(Rent)))
        Area.extend([None] * (max_length - len(Area)))

       # Creating  dataframe for the data scraped
        df = pd.DataFrame({
            'Location/Bldng_name': Location_Bldng_name,
            'Area': Area,
            'Rent': Rent
        })
      

      #dataframe saved to csv file
        df.to_csv('rentedplots.csv', index=False)
        time.sleep(2)
        

print('Data saved to rentedplots.csv')
driver.quit()
