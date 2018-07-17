# 爬虫模块
from lxml import etree

from .utils import get_page
from pyquery import PyQuery as pq
import re


class ProxyMetaclass(type):
    """
        元类，在FreeProxyGetter类中加入
        __CrawlFunc__和__CrawlFuncCount__
        两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):  # 爬虫类，用于抓取代理源网站的代理，用户可复写和补充抓取规则。
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies


    def crawl_kuaidaili(self):
        # 快代理
        print('快代理即将开始爬取')
        for page in range(1, 4):
            start_url = 'https://www.kuaidaili.com/ops/proxylist/{}/'.format(page)
            html = get_page(start_url)
            html_tree = etree.HTML(html)
            ip_s = html_tree.xpath('//div[@class="m-padding12"][3]//tbody[@class="center"]/tr/td[1]/text()')
            ips_post = html_tree.xpath('//div[@class="m-padding12"][3]//tbody[@class="center"]/tr/td[2]/text()')
            for ip_, ip_post in zip(ip_s, ips_post):
                yield 'http://' + ip_ + ':' + ip_post
    def crawl_xicidaili(self):
        # 西刺代理
        print('西刺代理即将开始爬取')
        for page in range(1,4):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(page)
            html = get_page(start_url)
            html_tree = etree.HTML(html)
            http_ips = html_tree.xpath('//table[@id="ip_list"]/tbody/tr/td[6]/text()')
            ip_s = html_tree.xpath('//table[@id="ip_list"]/tbody/tr/td[2]/text()')
            ips_post = html_tree.xpath('//table[@id="ip_list"]/tbody/tr/td[3]/text()')
            for http_ip, ip_, ip_post in zip(http_ips, ip_s, ips_post):
                yield http_ip + '://' + ip_ + ':' + ip_post


    def crawl_data5u(self):
        # DATA5U代理
        print('DATA5U代理即将开始爬取')
        for i in ['gngn', 'gwgn']:
            start_url = 'http://www.data5u.com/free/{}/index.shtml'.format(i)
            html = get_page(start_url)
            http_ips = re.findall('<ul class="l2">.*?<span.*?<a.*?<span.*?<li><a.*?>(.*?)</a>', html, flags=re.S)
            ip_s = re.findall('<ul class="l2">.*?<span><li>(.*?)</li>', html, flags=re.S)
            ips_post = re.findall('<ul class="l2">.*?<span.*?<span.*?<li class.*?>(.*?)</li>', html, flags=re.S)
            for http_ip, ip_, ip_post in zip(http_ips, ip_s, ips_post):
                yield http_ip + '://' + ip_ + ':' + ip_post

    def crawl_66http(self):
        # 66代理http
        print('66代理http即将开始爬取')
        start_url = 'http://www.66ip.cn/nmtq.php?getnum=&isp=0&anonymoustype=4&start=&ports=&export=&ipaddress=&area=0&proxytype=0&api=66ip'
        html = get_page(start_url)
        html_tree = etree.HTML(html)
        ips = ''.join(html_tree.xpath('/html/body/text()')).replace('\n', '').replace('\t\t', ',').replace('\t', '')
        ips = ips.split(',')
        for i in ips:
            ip_ = 'http://' + i
            yield ip_

    def crawl_66https(self):
        # 66代理https
        print('66代理https即将开始爬取')
        start_url = 'http://www.66ip.cn/nmtq.php?getnum=&isp=0&anonymoustype=4&start=&ports=&export=&ipaddress=&area=0&proxytype=1&api=66ip'
        html = get_page(start_url)
        html_tree = etree.HTML(html)
        ips = ''.join(html_tree.xpath('/html/body/text()')).replace('\n', '').replace('\t\t', ',').replace('\t', '')
        ips = ips.split(',')
        for i in ips:
            ip_ = 'https://' + i
            yield ip_


