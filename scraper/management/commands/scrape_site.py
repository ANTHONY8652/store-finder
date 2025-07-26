from django.core.management.base import BaseCommand
from scraper.models import Product
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class Command(BaseCommand):
    help = 'Scrape products from an example site'
    
    def handle(self, *args, **kwargs):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager).install(), options=options)

        try:
            self.stdout.write("Starting scrape please wait....")
            driver.get('https://naivas.online')
            driver.get('https://quickmart.co.ke')

            time.sleep(5)

            products = driver.find_elements(By.CSS_SELECTOR, '.product-card')

            for item in products:
                
                try:
                    name = item.find_element(By.CSS_SELECTOR, '.product-title').text
                    price_text = item.find_element(By.CSS_SELECTOR, '.product-price').text
                    url = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    price = float(price_text.replace('kes', ''). replace(',', '').strip())

                    Product.objects.update_or_create(
                        product_url=url,
                        defaults={
                            'name':name,
                            'price': price,
                            'source_site': 'naivas'
                        }
                    )

                    self.stdout.write(f'Saved: {name}')
                except Exception as e:
                    self.stderr.write(f'Error parsing item please try again: {e}')
                
        finally:
            driver.quit()
            self.stdout.write(self.style.SUCCESS("Scrapin finished done!."))
            