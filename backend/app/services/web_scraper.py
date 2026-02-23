import asyncio
import aiohttp
import newspaper
from bs4 import BeautifulSoup
import re
import logging
from typing import Dict, Any, Optional
from urllib.parse import urlparse, urljoin
import feedparser
from app.utils.validators import validate_url, extract_domain_from_url

logger = logging.getLogger(__name__)


class WebScraper:
    """Web scraping service for extracting article content from URLs"""
    
    def __init__(self):
        self._initialized = False
        self.session = None
        
        # User agent to avoid blocking
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        
        # Common content selectors
        self.content_selectors = [
            'article',
            '[class*="content"]',
            '[class*="article"]',
            '[class*="story"]',
            '[class*="post"]',
            'main',
            '.entry-content',
            '.post-content',
            '.article-content'
        ]
        
        # Common title selectors
        self.title_selectors = [
            'h1',
            '[class*="title"]',
            '[property="og:title"]',
            'title'
        ]
        
        # Common author selectors
        self.author_selectors = [
            '[class*="author"]',
            '[rel="author"]',
            '[class*="byline"]',
            '.author-name'
        ]
        
        # Common date selectors
        self.date_selectors = [
            '[datetime]',
            '[class*="date"]',
            '[class*="time"]',
            '[property="article:published_time"]'
        ]
    
    async def initialize(self):
        """Initialize the web scraper"""
        if self._initialized:
            return
        
        logger.info("Initializing Web Scraper...")
        
        # Create aiohttp session
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            headers={'User-Agent': self.user_agent}
        )
        
        self._initialized = True
        logger.info("Web Scraper initialized successfully")
    
    async def extract_article(self, url: str, extract_full_text: bool = True) -> Dict[str, Any]:
        """Extract article content from URL"""
        
        if not self._initialized:
            await self.initialize()
        
        try:
            # Validate URL
            validated_url = validate_url(url)
            
            # Try newspaper3k first (more reliable for news articles)
            article_data = await self._extract_with_newspaper(validated_url, extract_full_text)
            
            if not article_data.get("content"):
                # Fallback to manual extraction
                article_data = await self._extract_manually(validated_url, extract_full_text)
            
            # Post-process extracted data
            processed_data = self._post_process_article(article_data, validated_url)
            
            return processed_data
        
        except Exception as e:
            logger.error(f"Error extracting article from {url}: {e}")
            raise
    
    async def _extract_with_newspaper(self, url: str, extract_full_text: bool) -> Dict[str, Any]:
        """Extract article using newspaper3k library"""
        
        try:
            # Create article object
            article = newspaper.Article(url)
            
            # Configure
            article.config.browser_user_agent = self.user_agent
            article.config.request_timeout = 30
            article.config.fetch_images = False
            
            # Download and parse
            await asyncio.get_event_loop().run_in_executor(
                None, article.download
            )
            
            if not article.html:
                return {}
            
            await asyncio.get_event_loop().run_in_executor(
                None, article.parse
            )
            
            # Extract additional data if requested
            if extract_full_text:
                try:
                    await asyncio.get_event_loop().run_in_executor(
                        None, article.nlp
                    )
                except:
                    pass  # NLP extraction is optional
            
            # Build result
            result = {
                "title": article.title,
                "content": article.text,
                "author": article.authors[0] if article.authors else None,
                "publish_date": article.publish_date.isoformat() if article.publish_date else None,
                "source": article.source_url,
                "url": url,
                "summary": article.summary if hasattr(article, 'summary') else None,
                "keywords": article.keywords if hasattr(article, 'keywords') else [],
                "extraction_method": "newspaper3k"
            }
            
            return result
        
        except Exception as e:
            logger.warning(f"Newspaper3k extraction failed for {url}: {e}")
            return {}
    
    async def _extract_manually(self, url: str, extract_full_text: bool) -> Dict[str, Any]:
        """Extract article manually using BeautifulSoup"""
        
        try:
            # Fetch the page
            async with self.session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}: {response.reason}")
                
                html = await response.text()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract title
            title = self._extract_title(soup)
            
            # Extract content
            content = self._extract_content(soup)
            
            # Extract author
            author = self._extract_author(soup)
            
            # Extract publish date
            publish_date = self._extract_date(soup)
            
            # Extract summary (first paragraph)
            summary = ""
            if content:
                paragraphs = content.split('\n\n')
                if paragraphs:
                    summary = paragraphs[0].strip()
            
            result = {
                "title": title,
                "content": content,
                "author": author,
                "publish_date": publish_date,
                "source": extract_domain_from_url(url),
                "url": url,
                "summary": summary,
                "keywords": [],
                "extraction_method": "manual"
            }
            
            return result
        
        except Exception as e:
            logger.error(f"Manual extraction failed for {url}: {e}")
            return {}
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract article title"""
        
        for selector in self.title_selectors:
            elements = soup.select(selector)
            for element in elements:
                title = element.get_text(strip=True) or element.get('content', '')
                if title and len(title) > 10:  # Reasonable title length
                    return title
        
        return None
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract article content"""
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'advertisement']):
            element.decompose()
        
        # Try different content selectors
        for selector in self.content_selectors:
            elements = soup.select(selector)
            if elements:
                content_parts = []
                for element in elements:
                    text = element.get_text(strip=True)
                    if text:
                        content_parts.append(text)
                
                if content_parts:
                    return '\n\n'.join(content_parts)
        
        # Fallback: get all paragraphs
        paragraphs = soup.find_all('p')
        if paragraphs:
            content_parts = []
            for p in paragraphs:
                text = p.get_text(strip=True)
                if len(text) > 20:  # Filter out very short paragraphs
                    content_parts.append(text)
            
            if content_parts:
                return '\n\n'.join(content_parts)
        
        return ""
    
    def _extract_author(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract article author"""
        
        for selector in self.author_selectors:
            elements = soup.select(selector)
            for element in elements:
                author = element.get_text(strip=True) or element.get('content', '')
                if author and len(author) < 100:  # Reasonable author name length
                    return author
        
        return None
    
    def _extract_date(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract publish date"""
        
        for selector in self.date_selectors:
            elements = soup.select(selector)
            for element in elements:
                # Try datetime attribute first
                date_str = element.get('datetime') or element.get('content', '')
                if not date_str:
                    date_str = element.get_text(strip=True)
                
                if date_str:
                    # Try to parse and standardize date format
                    parsed_date = self._parse_date(date_str)
                    if parsed_date:
                        return parsed_date
        
        return None
    
    def _parse_date(self, date_str: str) -> Optional[str]:
        """Parse date string and return ISO format"""
        
        try:
            from datetime import datetime
            import dateutil.parser
            
            # Try parsing with dateutil (handles many formats)
            parsed = dateutil.parser.parse(date_str)
            return parsed.isoformat()
        
        except:
            # Try some common patterns manually
            patterns = [
                r'(\d{4}-\d{2}-\d{2})',
                r'(\d{2}/\d{2}/\d{4})',
                r'(\d{1,2}\s+\w+\s+\d{4})'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, date_str)
                if match:
                    return match.group(1)  # Return as-is, will be processed later
        
        return None
    
    def _post_process_article(self, article_data: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Post-process extracted article data"""
        
        # Clean content
        if article_data.get("content"):
            content = article_data["content"]
            # Remove excessive whitespace
            content = re.sub(r'\s+', ' ', content)
            # Remove common junk
            content = re.sub(r'(Read more|Continue reading|Click here).*$', '', content, flags=re.IGNORECASE)
            article_data["content"] = content.strip()
        
        # Clean title
        if article_data.get("title"):
            title = article_data["title"]
            # Remove site name from title
            title = re.sub(r'\s*[-|]\s*.*$', '', title)
            article_data["title"] = title.strip()
        
        # Add metadata
        article_data["domain"] = extract_domain_from_url(url)
        article_data["word_count"] = len(article_data.get("content", "").split())
        article_data["extracted_at"] = self._get_current_timestamp()
        
        # Validate minimum content
        if not article_data.get("content") or len(article_data["content"]) < 100:
            raise Exception("Insufficient content extracted")
        
        return article_data
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()
    
    async def extract_multiple_articles(self, urls: list) -> list:
        """Extract multiple articles concurrently"""
        
        if not self._initialized:
            await self.initialize()
        
        # Create tasks for concurrent extraction
        tasks = [
            self.extract_article(url, True) 
            for url in urls
        ]
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error processing URL {urls[i]}: {result}")
                processed_results.append({
                    "url": urls[i],
                    "error": str(result),
                    "success": False
                })
            else:
                processed_results.append({
                    **result,
                    "success": True
                })
        
        return processed_results
    
    async def get_domain_info(self, url: str) -> Dict[str, Any]:
        """Get information about the domain"""
        
        try:
            domain = extract_domain_from_url(url)
            
            # Basic domain info
            domain_info = {
                "domain": domain,
                "url": url,
                "protocol": urlparse(url).scheme,
                "subdomain": None
            }
            
            # Extract subdomain if present
            parts = domain.split('.')
            if len(parts) > 2:
                domain_info["subdomain"] = '.'.join(parts[:-2])
            
            # Try to get homepage title
            homepage_url = f"{urlparse(url).scheme}://{domain}"
            try:
                async with self.session.get(homepage_url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        title = soup.find('title')
                        if title:
                            domain_info["homepage_title"] = title.get_text(strip=True)
            except:
                pass
            
            return domain_info
        
        except Exception as e:
            logger.error(f"Error getting domain info for {url}: {e}")
            return {"domain": extract_domain_from_url(url), "error": str(e)}
    
    def get_domain(self, url: str) -> str:
        """Extract domain from URL (convenience method)"""
        
        return extract_domain_from_url(url)
    
    async def close(self):
        """Close the aiohttp session"""
        
        if self.session:
            await self.session.close()
            self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        
        return {
            "type": "web_scraper",
            "initialized": self._initialized,
            "features": [
                "article_extraction",
                "title_extraction",
                "author_extraction",
                "date_extraction",
                "domain_analysis"
            ],
            "extraction_methods": ["newspaper3k", "manual_beautifulsoup"]
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for the web scraper"""
        
        if not self._initialized:
            return {"status": "not_initialized"}
        
        try:
            # Test with a known URL
            test_url = "https://example.com"
            domain_info = await self.get_domain_info(test_url)
            
            return {
                "status": "healthy",
                "test_domain_info": domain_info,
                "session_active": self.session is not None
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
