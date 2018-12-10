import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from github.items import File

class GithubRepositoriesSpider(scrapy.Spider):
	name = 'repositories'


	def start_requests(self):
		#repositories = ['frontpressorg/frontpress']
		filename = '/home/amarel/vagas/github_scrapy/github/github/respositories.txt'
		repositories = [line.rstrip('\n') for line in open(filename)]
		for r in repositories:
			yield scrapy.Request(url='https://github.com/%s' % r, callback=self.parse)


	def parse(self, response):
		info = response.xpath('//div[@class="file-info"]/text()').extract()
		if info:
			item = File()
			item['url'] = response.url
			item['info'] = info
			item['filename'] = response.xpath('//strong[@class="final-path"]/text()').extract()[0]
			yield item
		for path in response.xpath('//td[@class="content"]//span[@class="css-truncate css-truncate-target"]/a/@href').extract():
			next_page = response.urljoin(path)
			yield scrapy.Request(next_page, callback=self.parse)
