# -*- coding: utf-8 -*-

# Scrapy settings for xspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'xspider'

SPIDER_MODULES = ['xspider.spiders']
NEWSPIDER_MODULE = 'xspider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

DOWNLOAD_DELAY = 0.25    # 250 ms of delay

ITEM_PIPELINES = {'xspider.pipelines.ImageDownloadPipeline': 1}

IMAGES_STORE = '/tmp/images/'
