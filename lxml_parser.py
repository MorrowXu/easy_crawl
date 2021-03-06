#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Morrow
# @IDE     : PyCharm
# @File    : lxml_parser.py
# @Email   : 464580843@qq.com
# Create on 2018/3/1 11:37
import re
try:
    import urlparse # python2.7
except ImportError:
    import urllib.parse as urlparse # python3.6
# from bs4 import BeautifulSoup as bs
from lxml import etree

class HtmlParser(object):
    """
    html源文件解析
    """

    def _get_new_urls(self, page_url, html):
        """
        解析url
        """
        new_urls = set()
        regex = re.compile(r'href="(/item/[\w%]+)"') # 取出a标签里符合的链接
        links = re.findall(regex, html) # 返回一个符合正则的url列表
        for link in links:
            new_full_url = urlparse.urljoin(page_url, link) # url自动补齐
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, html):
        """
        解析数据
        """
        res_data = {}
        res_data['url'] = page_url # url

        title_node = html.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()')
        res_data['title'] = title_node[0]

        summary_node = html.xpath('//div[@class="lemma-summary"]/div[@class="para"]/text()')
        para = '' # 段落
        for i in summary_node:para += i;
        res_data['summary'] = para
        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        html = etree.HTML(html_cont)
        new_urls = self._get_new_urls(page_url, html_cont)
        new_data = self._get_new_data(page_url, html)
        return new_urls, new_data
