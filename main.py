import logging
from datetime import datetime
import os
from config import OPENAI_API_KEY, is_article_recent, NEWSLETTER_TEMPLATE
from feed_processor import FeedProcessor
from article_extractor import ArticleExtractor
from content_generator import ContentGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to process feeds and generate newsletter."""
    try:
        # Initialize components
        feed_processor = FeedProcessor('sample_feeds.csv')
        article_extractor = ArticleExtractor()
        content_generator = ContentGenerator(OPENAI_API_KEY)
        
        # Load and process feeds
        feeds = feed_processor.load_feeds()
        newsletter_content = []
        processed_articles = 0
        
        for feed in feeds:
            logger.info(f"Processing feed: {feed['url']}")
            
            # Get articles from feed
            articles = feed_processor.parse_feed(feed['url'])
            logger.info(f"Found {len(articles)} articles in feed")
            
            # Process recent articles
            for article in articles:
                if not is_article_recent(article.get('published')):
                    continue
                
                logger.info(f"Processing article: {article['title']}")
                
                # Extract article content
                article_data = article_extractor.extract_article_text(article['link'])
                if not article_data:
                    logger.warning(f"Could not extract content from {article['link']}")
                    continue
                
                # Generate summary
                summary = content_generator.generate_summary(article_data['text'])
                if not summary:
                    logger.warning(f"Could not generate summary for {article['title']}")
                    continue
                
                # Format newsletter section
                section = content_generator.format_newsletter_section({
                    **article_data,
                    'source': article['source'],
                    'link': article['link']
                }, summary)
                
                newsletter_content.append(section)
                processed_articles += 1
                logger.info(f"Successfully processed article: {article['title']}")
        
        if processed_articles == 0:
            logger.warning("No articles were processed successfully")
            return
        
        # Format the complete newsletter
        date_str = datetime.now().strftime('%Y-%m-%d')
        complete_newsletter = NEWSLETTER_TEMPLATE.format(
            date=date_str,
            content="\n".join(newsletter_content)
        )
        
        # Save newsletter
        output_file = f"newsletter_{datetime.now().strftime('%Y%m%d')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(complete_newsletter)
        
        logger.info(f"Newsletter generated successfully: {output_file}")
        logger.info(f"Processed {processed_articles} articles")
        
    except Exception as e:
        logger.error(f"Error in main process: {e}")

if __name__ == "__main__":
    main()
