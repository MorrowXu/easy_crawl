#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Morrow
# @IDE     : PyCharm
# @File    : bs4_parser.py
# @Email   : 464580843@qq.com
# Create on 2018/3/5 15:13
import re
try:
    import urlparse # python2.7
except ImportError:
    import urllib.parse as urlparse # python3.6
from bs4 import BeautifulSoup as bs


class HtmlParser(object):
    """
    html源文件解析
    """

    def _get_new_urls(self, page_url, html_cont):
        """
        解析url
        """
        new_urls = set()
        # links = soup.find_all('a', href=re.compile(r"/item/[\w%]+$"))
        regex = re.compile(r'href="(/item/[\w%]+)"')
        links = re.findall(regex, html_cont)
        for link in links:
            new_full_url = urlparse.urljoin(page_url, link)  # url自动补齐
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        """
        解析数据
        """
        res_data = {}
        # url
        res_data['url'] = page_url

        # < dd class ="lemmaWgt-lemmaTitle-title" > < h1 > Request对象 < / h1 >
        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find('h1')
        res_data['title'] = title_node.get_text()

        # <div class="lemma-summary"
        summary_node = soup.find('div', class_='lemma-summary')
        res_data['summary'] = summary_node.get_text()

        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = bs(html_cont, 'lxml')
        new_urls = self._get_new_urls(page_url, html_cont)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
