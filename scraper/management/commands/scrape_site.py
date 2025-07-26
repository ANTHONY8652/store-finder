from django.core.management.base import BaseCommand
from scraper.models import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class Command(BaseCommand):
    help = 'Scrape Jumia, Quickmart and Naivas for search term or product needed.'

    def add_arguments(self, parser):
        parser.add_argument('--search_term', type=str, help='Keyword to search')

    def set_up_driver(self):
        opts = Options()
        opts.add_argument('--headless')
        opts.add_argument('--disable-gpu')
        opts.add_argument('--no-sandbox')
        
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = opts)
    
    def handle(self, *args, **kwargs):
        term = kwargs.get('search_term') or ''
        driver  = self.set_up_driver()

        try:
            self.scrape_jumia(driver, term)
            self.scrape_quickmart(driver, term)
            self.scrape_naivas(driver, term)
        
        finally:
            driver.quit()
        
        self.stdout.write(self.style.SUCCESS(f"Searching for {term} completed."))

    #SCraping Jumia is to only be used for research purposes and development phase and there arent a lot of known and reliable stores in Kenya Kilimall is great but fails in fields of customer satisfaction as well as order fulfillment and in that case we will only use jumia but when development is complete 
    #Jumia isn't in the official scope of the project it falls right outside the scope of the project sadly Usisahau kuitoa when done Anto please do not foget

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
                price = float(price_text.replace('Ksh', '').replace(',', '').strip())

                Product.objects.update_or_create(
                    product_url=url,
                    defaults = {
                        'name': name, 
                        'price': price, 
                        'source_site': 'Jumia', 'search_term': term}
                )
            
            except Exception as e:
                self.stderr.write(f"Jumia perse error: {e}")
    
    def scrape_quickmart(self, driver, term):
        if not term:
            return
        self.stdout.write("Scraping Quickmart please wait....")
        driver.get(f"https://quickmart.co.ke/shop/?s={term}&post_type=product")

        time.sleep(5)
        
        for item in driver.find_elements(By.CSS_SELECTOR, "li.product"):

            try: 
                name = item.find_element(By.CSS_SELECTOR, "h2.woocommerce-loop-product__title").text
                price_text = item.find_element(By.CSS_SELECTOR, ".price .amount").text
                url = item.find_element(By.CSS_SELECTOR, "a.woocommerce-LoopProduct-link").get_attribute('href')
                price = float(price_text.replace('Ksh', '').replace(',', '').strip())
                
                Product.objects.update_or_create(
                    product_url = url,
                    defaults={
                        'name': name,
                        'price': price,
                        'source_site': 'Quickmart',
                        'search_term': term
                    }
                )
            
            except Exception as e:
                self.stderr.write(f"Quickmart parse error: {e}")
    
    def scrape_naivas(self, driver, term):
        if not term:
            return
        self.stdout.write("Scrapig Naivas Supermarket....")
        driver.get(f"https://naivas.online/?s={term}&post_type=product")

        time.sleep(5)

        for item in driver.find_elements(By.CSS_SELECTOR, "li.product"):
            
            try:
                name = item.find_element(By.CSS_SELECTOR, "h2.woocommerce-loop-product__title").text
                price_text  = item.find_element(By.CSS_SELECTOR, ".price .amount").text
                url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                price = float(price_text.replace('Ksh', '').replace(',', '').strip())

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
            

