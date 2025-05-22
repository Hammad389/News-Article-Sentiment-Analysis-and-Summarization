Thanks Hammad — that helps clarify the issue.

You're using:

```python
tag.xpath("//div[@class='address-section']/a[@class='prop-link']/span[@class='address']/text()").getall()
```

### **Problem:**

You're starting the XPath with `//`, which means **search globally** in the entire document — so Scrapy returns **text from all matching spans on the page**.

---

### **Solution: Use `.` to make the XPath relative** to the current element (`tag`):

```python
tag.xpath(".//span[@class='address']/text()").getall()
```

This ensures:

* **Only the text inside the current span** is returned.
* You still get text from both before and after the `<br>`.

---

### **Full example (cleaned and joined):**

```python
address_parts = tag.xpath(".//span[@class='address']/text()").getall()
full_address = " ".join(part.strip() for part in address_parts if part.strip())
print(full_address)
```

---

Let me know if you're looping through multiple `div.address-section` blocks — I can help you structure that loop too.
