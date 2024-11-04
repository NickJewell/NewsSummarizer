import feedparser
from datetime import datetime
import pandas as pd
from typing import List, Dict
import logging
from email.utils import parsedate_to_datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedProcessor:
    def __init__(self, csv_path: str):
        """Initialize feed processor with CSV file path."""
        self.csv_path = csv_path
        
    def load_feeds(self) -> List[Dict]:
        """Load RSS feeds from CSV file."""
        try:
            df = pd.read_csv(self.csv_path)
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            return []

    def parse_feed(self, feed_url: str) -> List[Dict]:
        """Parse RSS feed and return recent articles."""
        try:
            feed = feedparser.parse(feed_url)
            if feed.bozo:
                logger.error(f"Error parsing feed {feed_url}: {feed.bozo_exception}")
                return []

            articles = []
            for entry in feed.entries:
                pub_date = self._parse_date(entry.get('published', ''))
                if pub_date:
                    article = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': pub_date,
                        'source': feed.feed.get('title', 'Unknown Source')
                    }
                    articles.append(article)
                
            return articles
        except Exception as e:
            logger.error(f"Error processing feed {feed_url}: {e}")
            return []

    def _parse_date(self, date_str: str) -> datetime:
        """Parse publication date string to datetime object."""
        if not date_str:
            return None
            
        try:
            # Try parsing RFC 2822 format first (common in RSS feeds)
            return parsedate_to_datetime(date_str)
        except:
            try:
                # Try ISO format
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except:
                return None
