#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2017 Eduardo Frazão ( https://github.com/fr4z40 )
# Last Update Vinnybr ~~~
#
#   Licensed under the MIT License;
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#

import robobrowser
import requests
from sys import argv
import warnings

warnings.filterwarnings("ignore")



header={
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive'
        }


s = requests.Session()
s.headers = header

session = robobrowser.RoboBrowser(history=True, session=s)



def file_handler(file_path, mode, content=None):

    handler = open(file_path, mode)

    if ((mode == 'r') or (mode == 'rb')):
        content = handler.read()
        handler.close()
        return(content)

    else:
        handler.write(content)
        handler.close()



def preencher_vaga(url):

    if '#nome_candidato' not in url:
        url = (url.strip('/')+'/#nome_candidato')

    session.open(url)
    form = session.get_forms()[1]

    for key in candidato_info:
        try:
            form[key].value = candidato_info[key]
        except:
            pass
			
    if 'anexo' in form.fields:
        form['forma_envio'] = 'anexo'
        form['anexo'] = open(cv_pdf, 'rb')
    else:
        try:
            form['forma_envio'] = 'curriculo'
            form['curriculo_candidato'] = cv_txt
        except:
            break;

    session.submit_form(form)


exec(file_handler('riovagas.form', 'r'))




######################################################

try:
    hst = ((file_handler('history.txt', 'r')).strip().split('\n'))
except:
    hst = []

pgn = 1

key = ('+'.join((argv[1]).split()))
url_base = ('https://www.riovagas.com.br/page/@PGN@/?s=%s&submit_x=0&submit_y=0' % key)


session.open(url_base.replace('@PGN@', str(pgn)))

try:
    last_page = int(session.find_all('a', {'class':'last'})[0].text)
except:
    last_page = int(session.find_all('a', {'class':'page'})[0].text)


links = session.find_all('a')

print('Key: %s' % key)
while pgn <= last_page:
    print('Page Number: %i' % pgn)
    links = list(filter((lambda x: type(x) != str), links))
    links = list(filter((lambda x: x.get('href') != None), links))
    links = list(filter((lambda x: '/riovagas/' in x.get('href')), links))
    links = list(set(map((lambda x: x.get('href')), links)))
    for lnk in links:
        if lnk not in hst:
            hst.append(lnk)
            file_handler('history.txt', 'a', (lnk+'\n'))
            print(lnk)
            preencher_vaga(lnk)
    pgn += 1
    if pgn > last_page:
        break
    else:
        new_url = url_base.replace('@PGN@', str(pgn))
        session.open(new_url)
        links = session.find_all('a')

print('\n')


