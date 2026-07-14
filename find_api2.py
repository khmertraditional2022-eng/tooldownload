import re
try:
    html = open('db_next_data.json', encoding='utf-8').read()
    urls = re.findall(r'[\"\'](https://[^\s\"\']+\.com[^\s\"\']*)[\"\']', html)
    api_urls = set([u for u in urls if 'api' in u or 'graphql' in u])
    print("API URLs:", api_urls)
except Exception as e:
    print(e)
