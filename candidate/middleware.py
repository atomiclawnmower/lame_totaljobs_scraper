#! -*- coding: utf-8 -*-

from scrapy.downloadermiddlewares.cookies import CookieJar, CookiesMiddleware


class CandidateCookiesMiddleware(CookiesMiddleware):

    def process_request(self, request, spider):

        if request.meta.get('clear_cookiejar', None):
            cookiejarkey = request.meta.get("cookiejar")
            self.jars[cookiejarkey] = CookieJar()
            request.meta['clear_cookiejar'] = False

        super(CandidateCookiesMiddleware, self)\
            .process_request(request, spider)


class RemoveDMCKey(object):

    def process_response(self, request, response, spider):
        if all(map(request.meta.get, ('dont_merge_cookies', 'one_way_dmc'))):
            request.meta['dont_merge_cookies'] = False
        return response