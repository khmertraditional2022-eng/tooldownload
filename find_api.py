import re

try:
    with open('db_next_data.json', encoding='utf-8') as f:
        html = f.read()
    apis = re.findall(r'[\"\'](https://[^\"\']*\.dramabox[^\.]*\.com/api/[^\"\']*)[\"\']', html)
    print("Found APIs:", set(apis))
    
    # Check for anything like /api/video/ or /api/book/
    apis2 = re.findall(r'[\"\'](/api/[^\"\']*)[\"\']', html)
    print("Found relative APIs:", set(apis2))
except Exception as e:
    print(e)
