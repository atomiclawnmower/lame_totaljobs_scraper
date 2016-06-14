# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from celery import save_user, save_last_processed, save_stopped
from scrapy.exceptions import DropItem
from .items import *

class CandidatePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, CandidateItem):
            if item['email'] and not ('Candidate' in item['name']):
                save_user.apply_async((item['name'], item['email']))
            else:
                raise DropItem()
        elif isinstance(item, LastProcessedItem):
            save_last_processed.apply_async((item['industry'],item['pageno']))
        elif isinstance(item, StoppedCategoryItem):
            save_stopped.apply_async((item['industry'], item['at'], item['pageno']))