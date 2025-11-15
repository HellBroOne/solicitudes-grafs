from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solicitudes.settings')
django.setup()

def before_scenario(context, scenario):
    """Se ejecuta antes de cada escenario"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    context.driver = webdriver.Chrome(options=chrome_options)
    context.driver.implicitly_wait(5)
    context.url = 'http://localhost:8000'

def after_scenario(context, scenario):
    """Se ejecuta después de cada escenario"""
    if hasattr(context, 'driver'):
        context.driver.quit()