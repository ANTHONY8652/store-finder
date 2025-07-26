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