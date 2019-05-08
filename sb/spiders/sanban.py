# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from subprocess import run
from time import sleep
from sb.items import ImageScrapeItem
from time import sleep
import urllib.request

id = input("Enter starting URL: ")
in_path = input("Enter path to download into: ")

class SanbanSpider(scrapy.Spider):
    name = 'sanban'
    allowed_domains = ['santabanta.com']
    start_urls = [id]

    def parse_page2(self, response):
    	img_url = response.xpath('//*[@id="wall"]/@src').extract_first()
    	arr = img_url.split('/')
    	path = in_path + arr[len(arr)-1]
    	sleep(2)
    	urllib.request.urlretrieve(img_url, path)
    	# yield {'img_url': [img_url]}


    def parse(self, response):
        # items = ImageScrapeItem()
        items = ImageScrapeItem()
        pics = response.xpath('//div[@class="wallpaper-big-1 position-rel"]/div[@class="wallpapers-box-300x180-2 wallpapers-margin-2"]')
        for pic in pics:
            # x = pic.extract().split('/')[3]
            x = pic.xpath('./div[@class="wallpapers-box-300x180-2-img"]/a/@href').extract_first()
            img_path = '/home/citizen/Downloads/temp/'
            url = 'http://www.santabanta.com/' +x+ '?high=6'
            print(url)
            yield scrapy.Request(url, dont_filter=True, callback=self.parse_page2)
            sleep(2)

        next = response.xpath('//*[@class="tsc_pagination tsc_paginationA tsc_paginationA08"]/li[last()]/a/@class').extract_first()
        if next is None:
        	return
        if next!='disabled':
        	next_pg_url = 'http://www.santabanta.com' + response.xpath('//*[@class="tsc_pagination tsc_paginationA tsc_paginationA08"]/li[last()]/a/@href').extract_first()
        yield scrapy.Request(next_pg_url, dont_filter=True)
        sleep(5)