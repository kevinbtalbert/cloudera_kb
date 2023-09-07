# Copyright 2023 Cloudera, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# XML PARSER AND WEB SCRAPER FOR INTERNAL LLM KNOWLEDGE BASE
# ASSUMES REQUISITE URLS AND SITE MAP SCHEMA ARE CONFIGURED IN
# cloudera_kb_config.conf FILE AND APPROPRIATE DEPENDENCIES
# ARE INSTALLED FROM PIP. 

# THE OUTPUT OF THIS FILE WILL STORE HTMLS IN /data WITH THE NAMING
# CONVENTION 1_htmls.txt FOR PARSING BY THE NEXT UTILITY

import requests
import configparser
from xml.etree import ElementTree as ET

config = configparser.ConfigParser()
config.read('cloudera_kb_config.conf')

from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urlparse, urljoin

visited_urls = set()

def get_tld(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def create_directory_path_from_url(base_path, url):
    url_parts = url.strip('/').split('/')
    directory_path = os.path.join(base_path, *url_parts[:-1])
    file_name = f"{url_parts[-1]}.txt"
    file_path = os.path.join(directory_path, file_name)
    return directory_path, file_path

def extract_and_write_text(url, base_path, tld):
    if url in visited_urls or not url.startswith(tld):
        return
    visited_urls.add(url)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    main_content = soup.find('main')

    if url.endswith('.html'):
            url = url[:-5]

    directory_path, file_path = create_directory_path_from_url(base_path, url)
    
    if main_content:
        os.makedirs(directory_path, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(soup.get_text())
            # for tag in main_content.find_all(True):
            #     if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span']:
            #         f.write(tag.get_text() + '\n')
            #     elif tag.name == 'table':
            #         for row in tag.find_all('tr'):
            #             row_data = [cell.get_text().strip() for cell in row.find_all(['td', 'th'])]
            #             f.write('\t'.join(row_data) + '\n')
            #         f.write('\n')
            #     elif tag.name in ['ol', 'ul']:
            #         for li in tag.find_all('li'):
            #             f.write(f'  - {li.get_text()}\n')
        
        # Recursive call for additional URLs within <main>
        for a_tag in main_content.find_all('a', href=True):
            new_url = urljoin(url, a_tag['href'])
            extract_and_write_text(new_url, base_path, tld)

def main():
    base_path = "./data/2_website_contents"
    with open("data/1_htmls.txt", "r") as file:
        for line in file:
            url = line.strip()
            if url:
                tld = get_tld(url)
                extract_and_write_text(url, base_path, tld)

if __name__ == '__main__':
    main()
