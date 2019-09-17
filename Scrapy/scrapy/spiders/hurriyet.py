# -*- coding: utf-8 -*-
import scrapy

informations = {} 
class HurriyetSpider(scrapy.Spider):
    name = 'hurriyet'
    allowed_domains = ['hurriyetemlak.com']
    start_urls = ['https://www.hurriyetemlak.com/kiralik-sahibinden?page=3']

    def parse(self, response):
        listview = response.css('div#listview')
        links = listview.css('a.overlay-link::attr("href")').extract()

        for home in links:
            home = response.urljoin(home)
            yield scrapy.Request(url=home , callback=self.parse_details)
            
            prev_page_url = response.css('a#lnkPrev::attr("href")').extract_first()
            if prev_page_url:
                prev_page_url = response.urljoin(prev_page_url)
                yield scrapy.Request(url=prev_page_url , callback=self.parse)

    def parse_details(self,response):
        informations.clear()
        price = response.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/div[2]/ul/li[1]/span//text()').extract_first()
        informations['Fiyat'] = price
        
        ilanNo = response.css('div.clearfix > ul.clearfix >  li.realty-numb > span::text').extract_first()
        ilanNo = ilanNo.split(':')[1].strip()
        informations['Ilan No'] = ilanNo
        
        adres =  response.css('div.clearfix > ul.clearfix >  li#realty-adress-line > span.address-line-breadcrumb > a')
        il = adres.css('a::text')[0].extract().strip()
        ilce = adres.css('a::text')[1].extract().strip()
        mahalle = adres.css('a::text')[2].extract().strip()

        informations['Il'] = il
        informations['Ilce'] = ilce
        informations['Mahalle'] = price

        info = response.css('div.clearfix > ul.clearfix > li.info-line > ul.clearfix > li')
        for i in info:
            if len(i.css('span::text').extract()) == 2:
                informations[i.css('span::text')[0].extract().strip()] =  i.css('span::text')[1].extract().strip()
        
        
        yield informations
        
