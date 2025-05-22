tags.xpath(".//div[@class='address-section']/a[@class='prop-link']/span[@class='address']").get().strip()
'<span class="address">\r\n                            1200 S. Conkling Street<br>Baltimore, MD 21224\r\n                        </span>'



address_parts = tags.xpath(".//span[@class='address']//text()").getall()
community_address = ' '.join(part.strip() for part in address_parts if part.strip())



 community_address = ' '.join(part.strip() for part in address_parts if part.strip())
>>> community_address
'1200 S. Conkling Street Baltimore, MD 21224 960 Southerly Rd. Towson, MD 21204 20 Lambourne Rd Towson, MD 21204 707 York Road Towson, MD 21204 1274 E Joppa Rd Towson, MD 21286 6809 Bellona Ave Baltimore, MD 21212 200 Foxhall Dr Bel Air, MD 21015'
