from openai import OpenAI
import json
import logging
from typing import Dict, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self, api_key: str):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=api_key)

    def generate_summary(self, article_text: str, max_words: int = 150) -> Optional[str]:
        """Generate article summary using OpenAI."""
        try:
            prompt = f"""
            Summarize the following article in a concise, engaging way. 
            Use no more than {max_words} words. 
            Focus on the key points and maintain a professional tone.
            Highlight any significant announcements, statistics, or industry trends.
            
            Article:
            {article_text}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Changed from gpt-4 to gpt-3.5-turbo
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return None

    def format_newsletter_section(self, article_data: Dict, summary: str) -> str:
        """Format article data and summary into newsletter section."""
        try:
            date_str = ""
            if article_data.get('publish_date'):
                date_str = f"\nPublished: {article_data['publish_date'].strftime('%Y-%m-%d %H:%M UTC')}"

            return f"""
## {article_data['title']}

{summary}

[Read full article]({article_data['link']})

*Source: {article_data['source']}*{date_str}

---
"""
        except Exception as e:
            logger.error(f"Error formatting newsletter section: {e}")
            return ""
