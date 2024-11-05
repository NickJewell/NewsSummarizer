from openai import OpenAI
import logging
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentEnhancer:

    def __init__(self, api_key: str):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=api_key)

    def read_newsletter(self, file_path: str) -> str:
        """Read the newsletter content from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading newsletter file: {e}")
            return None

    def extract_articles(self, content: str) -> list:
        """Extract individual articles from the newsletter content."""
        # Split content by '---' to separate articles
        articles = content.split('---')
        # Process each article to extract title and content
        processed_articles = []
        for article in articles:
            if '##' in article:  # Check if it contains a title
                title_match = re.search(r'##\s+(.+?)\n', article)
                title = title_match.group(1) if title_match else ""
                processed_articles.append({
                    'title': title,
                    'content': article.strip()
                })
        return processed_articles

    def select_top_stories(self, articles: list) -> list:
        """Use GPT-4 to analyze and select top 5 stories."""
        try:
            articles_text = "\n\n".join([
                f"Title: {a['title']}\nContent: {a['content']}"
                for a in articles
            ])
            prompt = f"""
            Analyze these news articles and select the top 5 most significant stories based on:
            1. Impact on the technology industry
            2. Potential long-term consequences
            3. Public interest and relevance
            4. Innovation and breakthrough factor

            Articles:
            {articles_text}

            Return only the titles of the top 5 articles in order of significance, formatted as a JSON array.
            """

            response = self.client.chat.completions.create(model="gpt-4",
                                                           messages=[{
                                                               "role":
                                                               "user",
                                                               "content":
                                                               prompt
                                                           }],
                                                           max_tokens=500,
                                                           temperature=0.7)

            top_titles = eval(response.choices[0].message.content.strip())
            return [
                article for article in articles
                if article['title'] in top_titles
            ]
        except Exception as e:
            logger.error(f"Error selecting top stories: {e}")
            return []

    def enhance_article(self, article: dict) -> str:
        """Create an enhanced, journalistic version of the article."""
        try:
            prompt = f"""
            Rewrite this tech news article in a more sophisticated, journalistic style consisting of absolutely no more than two solid paragraphs. 
            Focus on:
            1. Adding context and industry implications
            2. Professional tone and engaging narrative
            3. Clear structure with lead paragraph and supporting details
            4. Maintaining factual accuracy

            Original article:
            {article['content']}

            Provide the enhanced version maintaining the Markdown format with the original title.
            """

            response = self.client.chat.completions.create(model="gpt-4",
                                                           messages=[{
                                                               "role":
                                                               "user",
                                                               "content":
                                                               prompt
                                                           }],
                                                           max_tokens=1000,
                                                           temperature=0.7)

            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error enhancing article: {e}")
            return article['content']

    def save_enhanced_newsletter(self, enhanced_articles: list,
                                 output_path: str):
        """Save the enhanced newsletter to file."""
        try:
            date_str = datetime.now().strftime('%Y-%m-%d')
            header = f"""# Enhanced Tech News Newsletter for {date_str}

Welcome to today's carefully curated and enhanced tech news digest. These are the most significant stories of the day:

"""
            content = header + "\n\n".join(
                enhanced_articles) + "\n\n*Enhanced with AI assistance*"

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Enhanced newsletter saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving enhanced newsletter: {e}")
