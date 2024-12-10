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
