tags.xpath(".//div[@class='address-section']/a[@class='prop-link']/span[@class='address']").get().strip()
'<span class="address">\r\n                            1200 S. Conkling Street<br>Baltimore, MD 21224\r\n                        </span>'



address_parts = tags.xpath(".//span[@class='address']//text()").getall()
community_address = ' '.join(part.strip() for part in address_parts if part.strip())
