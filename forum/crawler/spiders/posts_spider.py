import scrapy
import datetime

class PostsSpider(scrapy.Spider):
	name = "posts"
	
	custom_settings = {
		'DOWNLOAD_DELAY': 1,
		'FEED_URI': 'forum_data.jl',
		'FEED_FORMAT': 'jsonlines',
		'FEED_EXPORT_ENCODING': 'utf-8',
		'LOG_FILE': 'errors.log',
#		'COOKIES_ENABLED': False,
#		'JOBDIR': 'crawls/posts_spider',
	}
	
	start_urls = ['http://forums.hababam.nl/index.php']
	min_date = datetime.datetime(2012, 11, 1)
	max_date = datetime.datetime(2016, 10, 31, 23, 59, 59)
	
	def parse(self, response):
		# follow links to subforums
		for href in response.css('li.forumbit_nopost h2.forumtitle a::attr(href)').extract():
			yield scrapy.Request(response.urljoin(href), callback=self.parse_subforum)
	
	def parse_subforum(self, response):
		# follow pagination link to next page of threads
		next_page = response.css('div.threadpagenav form.pagination span.prev_next a[rel="next"]::attr(href)').extract_first()
		last_post_date = response.css('ol.threads li.threadbit:not([id="thread_000001"]) dl.threadlastpost').xpath('./dd[2]/text()[1]').extract()[-1].strip()
		if not next_page is None and (last_post_date == 'Gisteren' or last_post_date == 'Vandaag' or datetime.datetime.strptime(last_post_date, '%d-%m-%Y') >= self.min_date):
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse_subforum)
		
		# follow links to threads
		for thread in response.css('ol.threads li.threadbit:not([id="thread_000001"])'):
			thread_title = thread.css('h3.threadtitle a.title')
			thread_last_post_date = thread.css('dl.threadlastpost').xpath('./dd[2]/text()[1]').extract_first().strip()
			if thread_last_post_date != 'Gisteren' and thread_last_post_date != 'Vandaag':
				thread_last_post_date = datetime.datetime.strptime(thread_last_post_date, '%d-%m-%Y')
				if thread_last_post_date <= self.max_date and thread_last_post_date >= self.min_date:
					meta = {
						'thread_title': thread_title.xpath('text()').extract_first(),
						'thread_category': response.css('div.pagetitle span.forumtitle::text').extract_first()
					}
					thread_url = response.urljoin(thread_title.xpath('@href').extract_first())
					yield scrapy.Request(thread_url, callback=self.parse_thread, meta=meta)
	
	def parse_thread(self, response):
		# follow pagination link to next page of posts
		next_page = response.css('ol.posts div.pagination_top form.pagination span.prev_next a[rel="next"]::attr(href)').extract_first()
		last_post_date = response.css('ol.posts li.postcontainer[id*="post"] div.posthead span.date::text').extract()[-1].strip()
		if not next_page is None and (last_post_date == 'Gisteren' or last_post_date == 'Vandaag' or datetime.datetime.strptime(last_post_date, '%d-%m-%Y') >= self.min_date):
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse_thread)
		
		# parse self
		yield from self.parse_posts(response)
	
	def parse_posts(self, response):
		def extract_with_css(post, query):
			return post.css(query).extract_first().strip()
		
		for post in response.css('ol.posts li.postcontainer[id*="post"]'):
			post_date = post.css('div.posthead span.date::text').extract_first().strip()
			if post_date != 'Gisteren' and post_date != 'Vandaag':
				post_date = datetime.datetime.strptime(post_date, '%d-%m-%Y')
				if post_date <= self.max_date and post_date >= self.min_date:
					user_image = post.css('a.postuseravatar img::attr(src)').extract_first()
					yield {
						'id': post.xpath('@id').extract_first(),
						'content': ' '.join(txt.strip() for txt in post.css('blockquote.postcontent::text').extract() if txt.strip()),
						'post_url': response.urljoin(extract_with_css(post, 'a.postcounter::attr(href)')), # fullview url for the post, easy for debugging
						'post_created_at': ' '.join(txt.strip() for txt in post.css('div.posthead span.date').xpath('.//text()').extract() if txt.strip()),
						'category': response.meta['thread_category'],
						'thread_url': response.url, # to get the ID postprocess this: response.url[response.url.rindex('t=')+2:]
						'thread_title': response.meta['thread_title'],
						'thread_post_number': extract_with_css(post, 'a.postcounter::text')[1:], # post number within the thread
						'user_gender': extract_with_css(post, 'div.username_container > img::attr(src)'),
						'user_name': ' '.join(txt.strip() for txt in post.css('a.username').xpath('.//text()').extract() if txt.strip()),
						'user_image': response.urljoin(user_image) if user_image else None, # some users do not have an avatar
						'user_postcount': max(post.css('dl.userinfo_extra dd.pbit2::text').re(r'(\d{1,3}(\.\d{1,3})*)'), key=len),
						'user_joined_at': extract_with_css(post, 'dl.userinfo_extra dd.pbit::text'),
					}
