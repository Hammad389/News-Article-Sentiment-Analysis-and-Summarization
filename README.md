# News Article Sentiment Analysis and Summarization

This repository contains a Python script that scrapes news articles from [The News](https://www.thenews.com.pk) based on a search query (e.g., entity name), performs sentiment analysis using the RoBERTa model, and summarizes the articles. The results are visualized in a clean and informative way.

## Features

- **Article Scraping**: Extracts news articles related to an entity by scraping them from The News website.
- **Sentiment Analysis**: Uses the RoBERTa model to analyze the sentiment of each article, categorizing it as Positive, Negative, or Neutral.
- **Summarization**: Summarizes each article using the BART model to provide a concise summary of the article.
- **Visualization**: Plots sentiment analysis results and displays summaries for each article in a well-organized manner.
- **Web Scraping with Selenium**: Handles dynamic content loading, ensuring that the scraping process works smoothly even when content is rendered by JavaScript.

## Requirements

To run the code, you will need the following libraries:

- `pandas`
- `matplotlib`
- `transformers`
- `requests`
- `bs4` (BeautifulSoup)
- `selenium`
- `scipy`
- `chromedriver_py`

You can install these dependencies using pip:

```bash
pip install pandas matplotlib transformers requests beautifulsoup4 selenium scipy chromedriver_py
```

## Setup

1. **Download ChromeDriver**: The script uses Selenium with the Chrome web browser. You need to have [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) installed and accessible on your system.
2. **Run the Script**: The script is designed to be run interactively, where you input the name of the entity you'd like to search for. The script will then proceed to:
   - Scrape the articles related to that entity.
   - Perform sentiment analysis on each article.
   - Provide a summary of each article.
   - Visualize the sentiment scores and summaries in a plot.

## Usage

### Running the script

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/news-article-sentiment-analysis.git
   cd news-article-sentiment-analysis
   ```

2. Run the Python script:
   ```bash
   python sentiment_analysis.py
   ```

3. Enter the entity name you want to search when prompted:
   ```bash
   Enter the name of the entity you want to search: Elon Musk
   ```

4. The script will scrape articles, perform sentiment analysis, and display visualizations with sentiment scores and article summaries.

## Functions

- **`process_input(user_input)`**: Processes the user input into a format suitable for a URL query.
- **`analyze_sentiment(article_body)`**: Analyzes the sentiment of the article text using the RoBERTa model.
- **`summarize_article(article_body)`**: Summarizes the article using the BART model.
- **`scrape_articles(search_entity)`**: Scrapes the articles related to the entity from The News website.
- **`data_visualizer(data_frame, search_entity)`**: Visualizes sentiment analysis results and article summaries in a grid format.

## Example Output

The script will generate a plot that contains:

1. A bar chart displaying sentiment scores (Negative, Neutral, Positive) for each article.
2. A text block containing the summary of the article.

Example:
(Searched for news articles about "open ai")
![Screenshot 2024-12-10 110044](https://github.com/user-attachments/assets/79cb41af-000a-444e-ae52-a32ba0d18f3d)

## Contributing

Feel free to fork the repository and make contributions. You can open an issue or submit a pull request if you'd like to contribute new features, improvements, or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



Perfect — let’s go through **your full code flow** to identify **why it's not reaching the data pages**, and why you're getting **empty files**. You're likely correct: **your spider is not making any recursive requests** due to one or more silent failures.

---

### ✅ Summary of what your spider should be doing:

1. Start at `https://www.udr.com/`
2. Extract city links → append `/map/`
3. Visit each `/map/` page → extract property links
4. Append `apartments-pricing/` → visit pricing page
5. Extract JS variable and parse data

---

## 🔍 Root Cause Analysis (with fixes)

---

### ❌ ISSUE #1: CSS selector for city links is wrong or fragile

You used:

```python
links = response.css("ul [class='cities'] >li>a::attr(href)").extract()
```

This selector is **invalid** due to:

* The wrong space (`ul [class=...]`) — it searches any descendant, not `ul.cities`
* `extract()` should be `getall()` (modern syntax)

#### ✅ Fix:

```python
links = response.css("ul.cities li a::attr(href)").getall()
```

---

### ❌ ISSUE #2: Incorrect `f-string` in:

```python
states_link = [f*{response.urljoin(link)}map/" for link in links]
```

* That’s a syntax error — `f*` is invalid
* Also you’re missing a `/` separator if `link` doesn’t end with `/`

#### ✅ Fix:

```python
states_link = [f"{response.urljoin(link)}map/" for link in links]
```

---

### ❌ ISSUE #3: Property page request is malformed

```python
yield scrapy.Request(un f"{link}apartments-pricing/", callback=...)
```

This line is invalid due to `un f` — it's probably a typo.

#### ✅ Fix:

```python
yield scrapy.Request(f"{link}apartments-pricing/", callback=self.apartments_pricing_scraper)
```

---

### ❌ ISSUE #4: CSS selector for property links may also be invalid

```python
response.css("div [class='address-section'] > a[class='prop-link']")
```

This is likely incorrect; should be:

```python
property_links = response.css("div.address-section a.prop-link::attr(href)").getall()
```

---

## ✅ Cleaned and Fully Functional `UrdSpider`

```python
import scrapy
import json
import re
from yourproject.items import ApartmentItem  # update with actual project name

class UrdSpider(scrapy.Spider):
    name = "urd"
    allowed_domains = ["udr.com"]
    start_urls = ["https://www.udr.com/"]

    def parse(self, response):
        # FIXED city link selector
        links = response.css("ul.cities li a::attr(href)").getall()
        states_link = [f"{response.urljoin(link)}map/" for link in links]

        for link in states_link:
            self.logger.info(f"State/City map page: {link}")
            yield scrapy.Request(link, callback=self.states_data_scraper)

    def states_data_scraper(self, response):
        # FIXED property link selector
        property_links = response.css("div.address-section a.prop-link::attr(href)").getall()
        complete_property_links = [response.urljoin(link) for link in property_links]

        for link in complete_property_links:
            pricing_url = f"{link}apartments-pricing/"
            self.logger.info(f"Visiting: {pricing_url}")
            yield scrapy.Request(pricing_url, callback=self.apartments_pricing_scraper)

    def apartments_pricing_scraper(self, response):
        # Search for the correct script dynamically
        scripts = response.css("script::text").getall()
        target_script = next((s for s in scripts if "window.udr.jsonObjPropertyViewModel" in s), None)

        if not target_script:
            self.logger.warning(f"No JSON script found on page: {response.url}")
            return

        # Extract JSON between two JS variables
        try:
            start_tag = "window.udr.jsonObjPropertyViewModel ="
            end_tag = "window.udr.localization ="
            start_index = target_script.index(start_tag) + len(start_tag)
            end_index = target_script.index(end_tag)
            json_str = target_script[start_index:end_index].strip().rstrip(";")
            formatted_data = json.loads(json_str)
        except Exception as e:
            self.logger.error(f"Error extracting JSON: {e}")
            return

        for data in formatted_data.get("floorPlans", []):
            units = data.get("units", [])
            if not units:
                continue
            unit = units[0]

            item = ApartmentItem(
                apartment_no=unit.get("marketingName"),
                no_of_bedrooms=unit.get("bedrooms"),
                no_of_bathrooms=unit.get("bathrooms"),
                area=unit.get("sqFt"),
                floor_no=unit.get("floorNumber"),
                availability=unit.get("isAvailable"),
                deposit=unit.get("deposit"),
                max_rent=unit.get("rentMin"),
                min_rent=unit.get("rentMax"),
                amenities=[a.get('value') for a in unit.get("amenities", [])],
            )
            yield item
```

---

### ✅ What to do next:

* Run with logging:

  ```bash
  scrapy crawl urd -L INFO
  ```
* Watch for logs like:

  ```
  Visiting: https://www.udr.com/.../apartments-pricing/
  ```
* Confirm JSON parsing logs show success or failure.

---

### Let Me Know:

If you can share the project folder name, I can plug it into the full code structure (items.py, settings.py) for you. Otherwise — fix the 4 issues above and it should run smoothly.

Let’s get it scraping!

