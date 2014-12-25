# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import csv
import requests
from scrapy import signals
from xspider import settings
import xlsxwriter


class XspiderPipeline(object):
    def process_item(self, item, spider):
        print('---------------------XspiderPipeline ----------------------')
        return item


class ImageDownloadPipeline(object):
    def process_item(self, item, spider):
        if spider.name not in ['meizitu']:
            return item
        print('---------------------ImageDownloadPipeline ----------------------')
        if 'image_urls' in item:
            dir_path = '%s/%s' % (settings.DATA_STORE, spider.name)

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            for image_url in item['image_urls']:
                print('---------------------download image: %s' % image_url)
                url = image_url.split('/')
                file_path = '%s/%s_%s_%s_%s' % (dir_path, url[-4], url[-3], url[-2], url[-1])
                if os.path.exists(file_path):
                    continue
                with open(file_path, 'wb') as handle:
                    response = requests.get(image_url, stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
        return item


class EbayItemPipeline(object):

    def __init__(self):
        print('---------------------EbayItemPipeline init----------------------')
        self.xlsx_file_name = 'items.xlsx'
        self.csv_file_name = 'items.csv'
        self.csv_file = csv.writer(open(self.csv_file_name, 'w'))


    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        print('---------------------EbayItemPipeline opened----------------------')
        self.csv_file.writerow(['Item ID', 'Title', 'Price', 'Sold', 'Country', 'Subtitle', 'Price Type', 'URL'])

    def spider_closed(self, spider):
        print('---------------------EbayItemPipeline closed----------------------')
        self.csv_to_xlsx(self.csv_file_name)

    def process_item(self, item, spider):
        if spider.name not in ['ebay']:
            return item
        print('---------------------EbayItemPipeline ----------------------')
        item_id = self.get_text(item.get('item_id'))
        url = self.get_text(item.get('url'))
        title = self.get_text(item.get('title'))
        # title = item['title']
        subtitle = self.get_text(item.get('subtitle'))
        price = self.get_text(item.get('price'))
        price_type = self.get_text(item.get('price_type'))
        extra = self.get_text_extra(item.get('extra'))
        country = self.get_text(item.get('country'))
        # print(item_id)
        # print(url)
        # print(title)
        # print(subtitle)
        # print(price)
        # print(price_type)
        # print(extra)
        # print(country)
        # print('\n')
        if extra is not None:
            row = [item_id, title, price, extra, country, subtitle, price_type, url]
            self.csv_file.writerow([unicode(s).encode('utf-8') for s in row])

        return item

    def get_text(self, item):
        if item and len(item) > 0:
            return item[0].strip()
        return ''

    def get_text_extra(self, item):
        if item and len(item) > 0:
            text = item[0].strip()
            # if 'sold' in text or 'watching' in text:
            if 'sold' in text and len(text) > 8:
                return text
        return None

    def csv_to_xlsx(self, csv_file):
        workbook = xlsxwriter.Workbook(self.xlsx_file_name)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 12)
        worksheet.set_column('B:B', 75)
        worksheet.set_column('C:C', 8)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('G:G', 13)
        worksheet.set_column('H:H', 15)
        reader = self.unicode_csv_reader(open(csv_file, 'rb'))
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                if r > 0 and c == 7:
                    worksheet.write_url(r, c, col, workbook.add_format({'color': 'blue', 'underline': 1}), u'点击我查看')
                else:
                    worksheet.write(r, c, col)
        workbook.close()
        workbook.close()

    def unicode_csv_reader(self, utf8_data, dialect=csv.excel, **kwargs):
        csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
        for row in csv_reader:
            yield [unicode(cell, 'utf-8') for cell in row]