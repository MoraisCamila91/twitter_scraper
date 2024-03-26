import re
from datetime import datetime

def get_info(texto):
    padrao_status = r'Account Live'
    padrao_username = r'Twitter username\n@([^\n]+)'
    padrao_description = r'Twitter Description\n(.+?)\n'
    padrao_email = r'Twitter email\n([^\n]+)'
    padrao_follower_count = r'Follower count\n([^\n]+)'
    padrao_date_create = r'Date Create\n(\w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \+\d{4} \d{4})'

    status = re.search(padrao_status, texto).group() if re.search(padrao_status, texto) else None
    username = re.search(padrao_username, texto).group(1) if re.search(padrao_username, texto) else None
    description = re.search(padrao_description, texto).group(1) if re.search(padrao_description, texto) else None
    email = re.search(padrao_email, texto).group(1) if re.search(padrao_email, texto) else None
    follower_count = re.search(padrao_follower_count, texto).group(1) if re.search(padrao_follower_count, texto) else None
    date_create = re.search(padrao_date_create, texto).group(1) if re.search(padrao_date_create, texto) else None

    if date_create:
        date_create = datetime.strptime(date_create, "%a %b %d %H:%M:%S %z %Y").strftime("%d/%m/%Y")
        
    return {"account_status": status,
            "username": username,
            "description": description,
            "email": email,
            "followers": follower_count,
            "date_creation": date_create}