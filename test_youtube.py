import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.scraper import scrape_youtube

url = "https://www.youtube.com/watch?v=BaW_jenozKc"
res = scrape_youtube(url)
print("Result:", res)
