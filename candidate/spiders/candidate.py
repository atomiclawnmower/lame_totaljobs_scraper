#! -*- coding: utf-8 -*-

from collections import defaultdict
from threading import Lock
from datetime import datetime
from time import sleep

from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider

from .. import formdata as fd, celery
from ..utils import *
from ..items import *


class CandidateSpider(Spider):

    name = 'candidate'
    start_urls = None

    lock = Lock()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        me = super(CandidateSpider, cls).from_crawler(crawler, *args, **kwargs)
        me.s = me.settings
        me.start_urls = [me.s['LOGIN_URL']]
        return me

    def __init__(self, *args, **kwargs):
        super(CandidateSpider, self).__init__(*args, **kwargs)
        self.rails = None
        self.restart_counter = 0
        self.started = datetime.now()
        self.last_processed = defaultdict(lambda: 1)
        self.no_nextpage = defaultdict(lambda: False)

    def populate_start_pages(self):
        sleep(5)
        lp = celery.get_last_processed.apply_async().get()
        lp = map(lambda a: (str(int(a[0])), int(a[1])), lp)
        self.last_processed.update(dict(lp))

    def _init_request(self, resp, owd, cookiejar, industry, page, **_):
        return FormRequest.from_response(
            resp,
            callback=self.login_success,
            formdata=fd.login(self.s['LOGIN'], self.s['PASSWORD']),
            meta={'cookiejar': cookiejar,
                  'industry': industry,
                  'one_way_dmc': owd,
                  'page': page},
            dont_filter=True
        )

    def parse(self, response):

        if self.s.get('RESTART') != '0':
            self.populate_start_pages()

        self.rails = sum(self.s['CATEGORIES'].values())

        i = 0
        for c, r in self.s['CATEGORIES'].items():

            for _ in range(r):
                yield self._init_request(
                    response, False, i, c, self.last_processed[c])
                i += 1

    def refresh_session(self, response):
        r = response
        self.logger.warning(
            "Re-login from cookiejar %s at page %s, industry %s",
            r.meta['cookiejar'], r.meta['page'], r.meta['industry'])

        self.restart_counter += 1
        if self.restart_counter == self.rails:
            self.restart_counter = 0
            self.started = datetime.now()

        yield self._init_request(r, True, **r.meta)

    def login_success(self, response):
        if not (self.s['SUCCESS_MARKER'] in response.css('title').extract()[0]):
            raise CloseSpider('Can\'t log in')

        response.meta['one_way_dmc'] = False

        yield Request(
            self.s['SEARCH_URL'],
            callback=self.search_form,
            meta=response.meta,
            dont_filter=True
        )

    def search_form(self, response):
        yield FormRequest.from_response(
            response,
            formdata=fd.search(response.meta['industry'], self.s["TIME_LIMIT"]),
            callback=self.switch_to_max_per_page,
            meta=response.meta,
            dont_filter=True
        )

    def switch_to_max_per_page(self, response):

        yield ExclusionFormRequest.from_response(
            response,
            formdata=fd.switch_to_max(),
            callback=self.switch_to_last_updated_ordering,
            exclude=self.s['EXCLUDED_FIELDS'],
            meta=response.meta,
            dont_filter=True
        )

    def switch_to_last_updated_ordering(self, response):

        yield ExclusionFormRequest.from_response(
            response,
            formdata=fd.switch_to_last(),
            callback=self.extract_candidates,
            exclude=self.s['EXCLUDED_FIELDS'],
            meta=response.meta,
            dont_filter=True
        )

    def extract_candidates(self, response):

        r = response
        industry, page = r.meta['industry'], r.meta['page']

        need_refresh = datetime.now() - self.started
        if need_refresh.seconds > self.s['SESSION_REFRESH_INTERVAL']*60:
            yield Request(
                url=self.start_urls[0],
                callback=self.refresh_session,
                dont_filter=True,
                meta={'cookiejar': response.meta['cookiejar'],
                      'industry': industry,
                      'page': page,
                      'download_timeout': self.s['SESSION_REFRESH_DELAY'],
                      'dont_merge_cookies': True}
            )

        has_next = response.xpath(self.s['NEXT_PAGE_XPATH']).re(r'(\d+)\'\)$')
        nextpage = None

        if has_next and (int(has_next[0]) < page) and\
                not(self.no_nextpage[industry]):
            nextpage = page

        if nextpage is None:
            with self.lock:
                if not self.no_nextpage[industry]:
                    nextpage = self.last_processed[industry]
                    self.last_processed[industry] += 1

        if not has_next:
            with self.lock:
                self.no_nextpage[industry] = True

            yield StoppedCategoryItem(
                at=datetime.now().isoformat(),
                industry=industry,
                pageno=page
            )

        if has_next and nextpage:

            yield ExclusionFormRequest.from_response(
                r,
                formdata=fd.next_candidate(str(nextpage)),
                callback=self.extract_candidates,
                exclude=self.s['EXCLUDED_FIELDS'],
                meta={'cookiejar': response.meta['cookiejar'],
                      'page': nextpage,
                      'industry': industry},
                dont_filter=True
            )

            yield LastProcessedItem(
                cookiejar=response.meta['cookiejar'],
                pageno=page,
                industry=industry
            )

            if not (nextpage % 100):
                search_data = " ".join(response.xpath(
                    '//div[@class="results-intro"]//text()').extract())\
                    .replace('\n', '').strip()

                self.logger.info("Search data at page %s: %s",
                                 nextpage, search_data)

        for row in response.xpath(self.s['ROW_XPATH']):
            email = row.xpath(self.s['EMAIL_XPATH']).extract_first()
            if email and email.endswith('.'):
                email = row.xpath(self.s['EMAIL_IN_ATTR_XPATH']).extract_first()
            person = CandidateItem()
            person['name'] = " ".join(row.xpath(self.s['NAME_XPATH']).extract())
            person['email'] = email
            yield person

