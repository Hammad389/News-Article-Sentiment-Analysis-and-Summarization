import scrapy


class UrdSpider(scrapy.Spider):
    name = "urd"
    allowed_domains = ["urd.com"]
    start_urls = ["https://urd.com"]

    # we can try to merge both functions
    def parse(self, response):
        links = response.css("ul [class='cities'] >li >a::attr(href)").extract()
        states_link = [f"{response.urljoin(link)}map/" for link in links]
        yield response.follow_all(states_link, callback=self.states_data_scraper)

    def states_data_scraper(self, response):
        property_links = response.css("div [class='address-section'] > a[class='prop-link']::attr(href)").extract()
        complete_property_links = [response.urljoin(link) for link in property_links]
        yield response.follow_all(complete_property_links, callback=self.property_data_scraper)

    def property_data_scraper(self, response):
        # Address
        property_name =  response.css("div [class='card-wrapper'] > div[class^='address-phone']> span ::text").extract()
        phone_no = response.css("div [class='card-wrapper'] > div[class^='address-phone'] div[class!='phone'] a ::text").extract()
        starting_prices = response.css("div [class='apartments-starting-prices']> ul >li[class='apt-starting-price-li'] ::text").extract()
        prices = [item.strip() for item in starting_prices if item.strip()]





