import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from github.items import File

class GithubRepositoriesSpider(scrapy.Spider):
	name = 'repositories'


	def __init__(self, **kwargs):
		super(GithubRepositoriesSpider, self).__init__(**kwargs)
		repositories = kwargs.get('repositories')
		self.start_urls = []
		for r in repositories:
			self.start_urls.append('https://github.com/%s' % r)


	def parse(self, response):
		#If it's a file path, 
		info = response.xpath('//div[@class="file-info"]/text()').extract()
		if info:
			item = File()
			item['url'] = response.url
			item['info'] = info
			item['filename'] = response.xpath('//strong[@class="final-path"]/text()').extract()[0]
			yield item
		else:
			for path in response.xpath('//td[@class="content"]//span[@class="css-truncate css-truncate-target"]/a/@href').extract():
				next_page = response.urljoin(path)
				yield scrapy.Request(next_page, callback=self.parse)
