from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

def get_shelter_info():
  # Set up Selenium WebDriver
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')  # Run in headless mode
  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
  
  links = []
  
  for page in range(1, 738):
    # Load the page
    driver.get(f"https://www.petfinder.com/animal-shelters-and-rescues/search/?page={page}")
    
    # Wait for dynamic content to load
    time.sleep(5)  # Adjust sleep time if necessary
    
    # Get the page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find the desired element
    main_section = soup.find('main').find('section', class_='tw-grid')
    
    if not main_section:
      print("Element not found")
    
    items = main_section.find_all('div', itemscrop=True)

    for item in items:
      a_tag = div.find('a')
      if a_tag and 'href' in a_tag.attrs:
        links.append(a_tag['href'])

  # Close the WebDriver
  driver.quit()

  return links

def extract_data_from_link(link):
  response = requests.get(link)
  soup = BeautifulSoup(response.text, 'html.parser')

  # Extract all text from the page
  page_text = soup.get_text()
  
  # Schelter or Rescue Name
  name_tag = soup.find('h1', class_='m-txt_alignLeft@minLg')
  name = name_tag.get_text(strip=True) if name_tag else 'N/A'
  
  # Web site url
  siteurl = 'N/A'
  url_div = soup.find('div', class_='m-media_gutterMd')
  if url_tag:
    siteurl = url_div.find('a')['href']

  # email
  email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' # Regular expression pattern for email addresses
  email = re.findall(email_pattern, page_text)
  
  # phone
  phone_span = soup.find('span', itemprop='telephone')
  phone = phone_span.get_text(strip=True) if phone_span else 'N/A'

  # address
  address = 'N/A'
  address_tag = soup.find('div', itemprop='address')
  if address_tag:
    address = address_tag.find('span', itemprop='addressLocality').get_text(strip=True) + address_tag.find('span', itemprop='addressRegion')

  return {
    'name': name,
    'siteurl': siteurl,
    'email': email,
    'phone': phone,
    'address': address
  }

def main():
  shelter_links = get_shelter_info()

  data_list = []
  for link in shelter_links:
    print(f"Extracting data from: {link}")
    data = extract_data_from_link(link)
    data_list.append(data)

  # Convert the list of dictionaries to a pandas DataFrame
  df = pd.DataFrame(data_list)
    
  # Save the DataFrame to an Excel file
  df.to_excel('shelter_data.xlsx', index=False)

if __name__ == "__main__":
  main()