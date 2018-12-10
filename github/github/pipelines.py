# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter
#from urllib.parse import unquote
import urllib2
import re
import os

#Check if a string number is float in cases like '2.31KB'
def isDigit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


#check if the size is in kb and convert it if necessary
def convert_to_bytes(value, info):
	if 'KB' in info:
		return int(value * 1024)
	return int(value)


def get_lines(info):
	return [int(s) for s in info.split() if isDigit(s)][0]


def get_bytes(info):
	_bytes = [float(s) for s in info.split() if isDigit(s)][0]
	return convert_to_bytes(_bytes, info)

def get_path(full_path):
	path = re.split(r"/", full_path)[:-1]
	if 'blob' in path: 
		path.remove('blob')
	if 'master' in path: 
		path.remove('master')
	return path



class FileInfosPipeline(object):
	def process_item(self, item, spider):
		if len(item['info']) == 2:
			#if file with line and size in the description
			item['lines'] = get_lines(item['info'][0])
			item['_bytes'] = get_bytes(item['info'][1])
		elif len(item['info']) == 4:
			#if is a executable file
			item['lines'] = get_lines(item['info'][2])
			item['_bytes'] = get_bytes(item['info'][3])
		elif len(item['info']) == 3:
			#if is a executable file without lines lenght
			item['lines'] = 0
			item['_bytes'] = get_bytes(item['info'][2])
		else:
			#if file description dont have lines lenght
			item['lines'] = 0
			item['_bytes'] = get_bytes(item['info'][0])
		item['full_path'] = urllib2.unquote(item['url'][19:])
		item['path'] = get_path(item['full_path'])
		temp_filename, file_extension = os.path.splitext(item['full_path'])
		item['file_extension'] = '<outros>' if file_extension == '' else file_extension[1:]
		item['repository'] = '/'.join(item['path'][:2])
		return item



class JsonWriterPipeline(object):

    file = None

    def open_spider(self, spider):
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.file = open(os.path.join(basedir, 'items.json'), 'w')
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item