Single Domain Web Scraper POC

Based on Scrapy: 
	http://scrapy.org/
	https://github.com/scrapy/scrapy

What it does:
	Crawls a single domain to a defined depth and returns a list of all links found.

How to use it:
	Install:
		Install Python 3+
		Install scrapy
			Linux>pip install scrapy
			Windows/Anaconda>conda install -c scrapinghub scrapy
			Note that standard pip on Windows appears to miss a number of dependencies and files.
	Set your target:
		Edit single_domain_spider.py and update the start_urls list
	Run it:
		Open a command prompt
		Navigate into the single_domain directory
		>scrapy crawl SDSpider -s DEPTH_LIMIT=#
			where # is a depth to your choosing - use 2 for a quick test; emit for a full scan