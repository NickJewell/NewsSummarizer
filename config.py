import os
from datetime import datetime, timedelta
import pytz

# OpenAI Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Feed Processing Configuration
MAX_DAYS_OLD = 7
BATCH_SIZE = 10

# Output Configuration
NEWSLETTER_TEMPLATE = """
# Tech News Newsletter for {date}

Welcome to today's curated tech news digest. Here are the latest stories from top tech sources:

{content}

*Generated with AI assistance*
"""

ARTICLE_TEMPLATE = """
## {title}

{summary}

[Read full article]({link})

*Source: {source}*
{date_str}

---
"""

def is_article_recent(article_date):
    """Check if article is within the last MAX_DAYS_OLD days."""
    if not article_date:
        return False
    # Convert current time to UTC for comparison
    cutoff_date = datetime.now(pytz.UTC) - timedelta(days=MAX_DAYS_OLD)
    return article_date > cutoff_date
