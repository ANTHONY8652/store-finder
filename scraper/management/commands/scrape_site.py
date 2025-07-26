from django.core.management.base import BaseCommand
from scraper.models import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def clean_price(price_str):
    try:
        price_str = price_str.replace("Ksh", "").replace("KSH", "").replace("KSh", "")
        price_str = price_str.replace(",", "").replace(" ", "").strip()
        if price_str == "":
            return None
     
        return float(price_str)
        
    except (ValueError, AttributeError):
            return None

class Command(BaseCommand):
    help = 'Scrape Jumia, Quickmart and Naivas for search term or product needed.'

    def add_arguments(self, parser):
        parser.add_argument('--search_term', type=str, help='Keyword to search')

    def set_up_driver(self):
        opts = Options()
        #opts.add_argument('--headless')
        opts.add_argument('--disable-gpu')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-software-rasterizer')
        
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = opts)
    
    def handle(self, *args, **kwargs):
        term = kwargs.get('search_term') or ''
        driver  = self.set_up_driver()

        try:
            #self.scrape_jumia(driver, term)
            self.scrape_quickmart(driver, term)
            self.scrape_naivas(driver, term)
        
        finally:
            driver.quit()
        
        self.stdout.write(self.style.SUCCESS(f"Searching for {term} completed."))
            

#Jumia is not in thw final scope of the project it also keep throttling me and rate limiting me I am done with it


    """
    def scrape_jumia(self, driver, term):
        if not term:
            return 
        self.stdout.write("Scraping Jumia")
        driver.get(f"https://jumia.co.ke/catalog/?q={term}")

        time.sleep(5)

        for item in driver.find_elements(By.CSS_SELECTOR, 'article.prd'):
            try:
                name = item.find_element(By.CSS_SELECTOR, '.info .name').text
                price_text = item.find_element(By.CSS_SELECTOR, '.info .prc').text
                url = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                price = clean_price(price_text)

                Product.objects.update_or_create(
                    product_url=url,
                    defaults = {
                        'name': name, 
                        'price': price, 
                        'source_site': 'Jumia', 'search_term': term}
                )
            
            except Exception as e:
                self.stderr.write(f"Jumia perse error: {e}")
    """  
    
    def scrape_quickmart(self, driver, term):
        if not term:
            return
        self.stdout.write("Scraping Quickmart please wait....")
        driver.get(f"https://quickmart.co.ke/products/search?keyword-{term}&pagesize-10")

        time.sleep(5)

        containers = driver.find_elements(By.CLASS_NAME, "products-foot")
        
        for container in containers:
            try:
                link = container.find_element(By.CLASS_NAME, "products-title")
                name = link.text
                url = link.get_attribute("href")

                price_element = container.field_element(By.CLASS_NAME, "product-price")
                raw_price = price_element.text.strip()
                price = clean_price(raw_price)
            
                Product.objects.update_or_create(
                    product_url = url,
                    defaults = {
                        "name": name,
                        "price": price,
                        "source_site": "Quickmart",
                        "search_term": term
                    }
                )
                self.stdout.write(f"Saved: {name} - {price}")
            
            except Exception as e:
                self.stderr.write(f"Error parsing product: {e}")
          
    
    def scrape_naivas(self, driver, term):
        if not term:
            return
        self.stdout.write("Scraping Naivas Supermarket....")
        driver.get(f"https://naivas.online/search?term={term}")

        time.sleep(5)

        for item in driver.find_elements(By.CSS_SELECTOR, "li.product"):
            
            try:
                name = item.find_element(By.CSS_SELECTOR, "h2.woocommerce-loop-product__title").text
                price_text  = item.find_element(By.CSS_SELECTOR, ".price .amount").text
                url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                price = clean_price(price_text)

                Product.objects.update_or_create(
                    product_url = url,
                    defaults = {
                        'name':name,
                        'price': price,
                        "source_site": "Naivas",
                        'search_term': term
                    }
                )
            except Exception as e:
                self.stderr.write(f"Naivas parse erra: {e}")
