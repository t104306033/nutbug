# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 23:54:26 2017

@author: VX
"""

import os
import requests
from bs4 import BeautifulSoup




def download(filename, src_url):
    try:
        src_res = requests.get(src_url, stream=True)
        soup = BeautifulSoup(src_res.text, "lxml")
        paper_url = soup.body.div.p.a['href']
        
        print(paper_url)
        paper_res = requests.get(paper_url, stream=True)
        filename = filename
        with open(filename, 'wb') as f:
            f.write(paper_res.content)
        print("{} Completed".format(filename))
    except Exception as e:
        print(e.message, e.args)
        return (filename, src_url)
    return None


if __name__=='__main__':
    file_dir = '/home/wei/good/'
    os.chdir(file_dir)
    print(os.getcwd())
    
    
    src_url_root = "https://www.sciencedirect.com/"
    
    fail = []
    #user_agent = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
    main_page = 'https://www.sciencedirect.com/search?qs=ORC&origin=article&zone=qSearch&years=2018%2C2017%2C2016%2C2015&offset=0'
    main_res = requests.get(main_page)
    soup = BeautifulSoup(main_res.text, "lxml")
    paper_area = soup.select('div[class="ResultList col-xs-24"]')[0]
    paper_blocks = paper_area.select('div[class="result-item-content"]')
    titles = []
    for paper_block in paper_blocks:
        title = paper_block.select('h2 a')[0].text
        attr = paper_block.select('ol[class="SubType hor"]')[0].text
        date = attr.split(',')[2]
        date_year = date.split()[1]
        src_url_index = paper_block.select('li[class="DownloadPdf download-link-item"]')[0].a['href']
        src_url = src_url_root + src_url_index
        err = download(title, src_url)
        fail.append(err)
    print(fail)

