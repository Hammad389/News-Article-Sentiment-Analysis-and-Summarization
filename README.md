for tags in response.css("div.property-card"):  # not the parent wrapper
    community_link = response.urljoin(tags.css("div.address-section a.prop-link::attr(href)").get())
    community_name = tags.css("div.address-section a.prop-link span.prop-name::text").get()

    # Relative XPath scoped to just this tag
    address_parts = tags.xpath(".//span[@class='address']//text()").getall()
    community_address = ' '.join(part.strip() for part in address_parts if part.strip())

    print("✅ Address:", community_address)
