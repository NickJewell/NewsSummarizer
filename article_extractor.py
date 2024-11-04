from newspaper import Article
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArticleExtractor:
    @staticmethod
    def extract_article_text(url: str) -> Optional[str]:
        """Extract article text using newspaper3k."""
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            # Return both title and text
            return {
                'title': article.title,
                'text': article.text,
                'authors': article.authors,
                'publish_date': article.publish_date
            }
        except Exception as e:
            logger.error(f"Error extracting article from {url}: {e}")
            return None
