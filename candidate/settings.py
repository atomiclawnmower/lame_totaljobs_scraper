# -*- coding: utf-8 -*-
###################
# PARSING         #
# PARAMETERS      #
###################

CATEGORIES = {
    # Category settings
    # Category no: category priority (== number of asyncronous 'rails')
}

# Session refresh (re-login) interval (min)
SESSION_REFRESH_INTERVAL = 15
# Delay before re-login (sec.)
SESSION_REFRESH_DELAY = 15

### User settings
LOGIN = ''
PASSWORD = ''

###  Database Settings
DB_LOGIN = ''
DB_NAME = ''
DB_PASSWORD = ''

### Search depth settings
"""
from 1 to 5 - N days
6 - 1 week
7 - 2 weeks
8 - 1 month
9 - 2 months
10 - 3 months
11 - 6 months
14 - 1 year
15 - 1,5 years
0 - no time limit
"""
TIME_LIMIT = '0'

###################
# PARSER SETTINGS #
###################
LOGIN_URL = 'https://recruiter.totaljobs.com/login'

SEARCH_URL = 'https://recruiter.totaljobs.com/Recruitment/CandidateSearch/CandidateSearch.aspx'

###################
# SCRAPY SETTINGS #
###################
BOT_NAME = 'candidate'

SPIDER_MODULES = ['candidate.spiders']
NEWSPIDER_MODULE = 'candidate.spiders'

LOG_LEVEL = 'INFO'

LOG_FORMATTER = 'candidate.utils.SilentDropFormatter'

REACTOR_THREADPOOL_MAXSIZE = 5

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'

CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 0.3

CONCURRENT_REQUESTS_PER_DOMAIN = 32

DOWNLOADER_MIDDLEWARES = {
    'candidate.middleware.RemoveDMCKey': 100
}

ITEM_PIPELINES = {
    'candidate.pipelines.CandidatePipeline': 300,
}

import os.path as op
LOG_FILE = op.abspath(op.join(op.dirname(__file__), '..', 'run.log'))

###################
# CELERY SETTINGS #
###################


###################
# OTHER SETTINGS  #
###################

SUCCESS_MARKER = 'Recruiter Dashboard'

ROW_XPATH = '//div[@class="row card-row"]'
NAME_XPATH = './/a[@class="candidate-lnk"]//text()'
EMAIL_XPATH = './/a[contains(@class,"email-candidate")]/text()'
EMAIL_IN_ATTR_XPATH = './/a[contains(@class,"email-candidate")]/@data-content'

NEXT_PAGE_XPATH = '//li[@class="paging-forward"]/a/@href'

EXCLUDED_FIELDS = (
    'ctl00$cphCentralPanel$ucSearchResults$ucRefineSearch$ddlIndustries',
    'ctl00$cphCentralPanel$ucSearchResults$ucRefineSearch$ddlMaxValue',
    'ctl00$cphCentralPanel$ucSearchResults$ucRefineSearch$ddlMinValue',
    'ctl00$cphCentralPanel$ucSearchResults$ucRefineSearch$ddlResidence',
    'ctl00$cphCentralPanel$ddlExistingSearches',
    'ctl00$cphCentralPanel$ucSearchResults$ucRefineSearch$ddlLanguages',
    'ctl00$cphCentralPanel$btnSave'
)
