# -*- coding: utf-8 -*-

# Scrapy settings for CERL_HCD_IE project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'CERL_HCD_IE'

SPIDER_MODULES = ['CERL_HCD_IE.spiders']
NEWSPIDER_MODULE = 'CERL_HCD_IE.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'CERL_HCD_IE (+http://www.yourdomain.com)'

DEPTH_LIMIT = 1
DOWNLOAD_DELAY = .1