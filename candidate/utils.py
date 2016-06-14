#! -*- coding: utf-8 -*-

from scrapy import FormRequest, log, logformatter

class ExclusionFormRequest(FormRequest):

    def __init__(self, *args, **kwargs):
        formdata = kwargs.pop('formdata', None)
        exclude = kwargs.pop('exclude', [])
        if formdata is not None:
            formdata = [(k, v) for k, v in formdata if k not in exclude]
        kwargs['formdata'] = formdata
        super(ExclusionFormRequest, self).__init__(*args, **kwargs)


class SilentDropFormatter(logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        return {
            'level': log.DEBUG,
            'format': logformatter.DROPPEDMSG,
            'exception': exception,
            'item': item
        }