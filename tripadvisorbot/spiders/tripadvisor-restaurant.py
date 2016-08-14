import re
import time

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request

from tripadvisorbot.items import *
from tripadvisorbot.spiders.crawlerhelper import *


# Constants.
# Max reviews pages to crawl.
# Reviews collected are around: 5 * MAX_REVIEWS_PAGES
MAX_REVIEWS_PAGES = 500

GEO = {"Paris": 187147, "Lyon": 187265}
CAT = {"Coffee": 9900, "Restaurant": 10591, "Dessert": 9909, "Bakery": 9901, "Bars": 11776}


class TripAdvisorRestaurantBaseSpider(BaseSpider):
	name = "tripadvisor-restaurant"

	allowed_domains = ["tripadvisor.com"]
	base_uri = "https://www.tripadvisor.com"
	start_urls = [
		base_uri + "/RestaurantSearch?Action=PAGE&geo=187265&ajax=1&itags=10591&sortOrder=popularity&availSearchEnabled=true"
	    # base_uri + "/RestaurantSearch?Action=PAGE&geo=187265&ajax=1&itags=10591&sortOrder=popularity&availSearchEnabled=true&o=a660"
	]

	# Building index urls for this location
	def parse(self, response):
		sel = Selector(response)
		last_page = int(clean_parsed_string(get_parsed_string(sel.xpath('//div[@class="pageNumbers"]'), 'a[position()=last()]/text()')))
		for i in range(last_page):
			id_page = str(i*30)
			url = response.url + '&o=a'+id_page
			print('*******************************', url)
			yield Request(url=url, callback=self.parse_result)

	# Page type: /RestaurantSearch
	def parse_result(self, response):
		tripadvisor_items = []

		sel = Selector(response)

		snode_restaurants = sel.xpath('//div[@id="EATERY_SEARCH_RESULTS"]/div[starts-with(@class, "listing")]')
		
		# Build item index.
		for snode_restaurant in snode_restaurants:

			tripadvisor_item = TripAdvisorItem()
			tripadvisor_item['name'] = clean_parsed_string(get_parsed_string(snode_restaurant, 'div[starts-with(@class,"shortSellDetails")]/h3[@class="title"]/a[@class="property_title"]/text()'))
			tripadvisor_item['url'] = self.base_uri + clean_parsed_string(get_parsed_string(snode_restaurant, 'div[starts-with(@class,"shortSellDetails")]/h3[@class="title"]/a[@class="property_title"]/@href'))

			# Populate address and contact info for current item.
			yield Request(url=tripadvisor_item['url'], meta={'tripadvisor_item': tripadvisor_item}, callback=self.parse_search_page, dont_filter=True)

			tripadvisor_items.append(tripadvisor_item)

	# Popolateaddress and contact info in item index for a single item.
	def parse_search_page(self, response):
		tripadvisor_item = response.meta['tripadvisor_item']
		sel = Selector(response)

		# TripAdvisor address and contact infos for item.
		snode_address = sel.xpath('//div[@class="info_wrapper restaurant"]')
		tripadvisor_address_item = TripAdvisorAddressItem()

		tripadvisor_address_item['street'] = clean_parsed_string(get_parsed_string(snode_address, 'address/span/span[@class="format_address"]/span[@class="street-address"]/text()'))

		snode_address_postal_code = clean_parsed_string(get_parsed_string(snode_address, 'address/span/span[@class="format_address"]/span[@class="locality"]/span[@property="postalCode"]/text()'))
		if snode_address_postal_code:
			tripadvisor_address_item['postal_code'] = snode_address_postal_code

		snode_address_locality = clean_parsed_string(get_parsed_string(snode_address, 'address/span/span[@class="format_address"]/span[@class="locality"]/span[@property="addressLocality"]/text()'))
		if snode_address_locality:
			tripadvisor_address_item['locality'] = snode_address_locality

		snode_phone = get_parsed_string(snode_address, 'div[@class="contact_info"]/div[@class="odcHotel blDetails"]/div[position() = 1]/div[@class="fl phoneNumber"]/text()')
		if snode_phone:
			tripadvisor_address_item['phone'] = snode_phone

		tripadvisor_address_item['email'] = split_mail(get_parsed_string(snode_address, 'div[@class="contact_info"]/div[@class="odcHotel blDetails"]/div[position() = last()]/div[@class="taLnk fl"]/@onclick'))

		tripadvisor_item['address'] = tripadvisor_address_item

		yield tripadvisor_item
