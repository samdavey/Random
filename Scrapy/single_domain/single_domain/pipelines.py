# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FilesPipeline(object):
    def process_item(self, item, spider):
        print(">>> I found item ", item, " with spider ", spider)
        return item
