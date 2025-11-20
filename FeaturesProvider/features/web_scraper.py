"""
Web scraper module for extracting job posting content from URLs.
Implements a hybrid approach: tries simple HTTP requests first, falls back to browser automation if needed.
"""

import re
from typing import Optional
import requests
from bs4 import BeautifulSoup, Tag
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


class ScrapingError(Exception):
    """Raised when URL scraping fails."""
    pass


def _clean_text(text: str) -> str:
    """Clean extracted text by removing excessive whitespace and normalizing."""
    # Replace multiple whitespaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Replace multiple newlines with double newline
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()


def _extract_main_content(soup: BeautifulSoup) -> str:
    """
    Extract main content from parsed HTML, filtering out navigation, footer, and ads.
    """
    # Remove script, style, nav, footer, and common ad elements
    for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
        element.decompose()

    # Remove common ad and tracking elements by class/id
    ad_patterns = ['ad', 'advertisement', 'banner', 'cookie', 'popup', 'modal']
    for pattern in ad_patterns:
        for element in soup.find_all(class_=re.compile(pattern, re.I)):
            element.decompose()
        for element in soup.find_all(id=re.compile(pattern, re.I)):
            element.decompose()

    # Try to find main content area
    main_content = None

    # Common main content selectors
    content_selectors = [
        ('main', {}),
        ('article', {}),
        ('div', {'role': 'main'}),
        ('div', {'id': re.compile(r'(main|content|job|position|description)', re.I)}),
        ('div', {'class': re.compile(r'(main|content|job|position|description)', re.I)}),
    ]

    for tag, attrs in content_selectors:
        main_content = soup.find(tag, attrs)
        if main_content:
            break

    # Fallback to body if no main content found
    if not main_content:
        main_content = soup.find('body')

    if not main_content:
        return ""

    # Extract text with paragraph separation
    text_parts = []
    for element in main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'div']):
        if isinstance(element, Tag):
            text = element.get_text(strip=True)
            if text and len(text) > 10:  # Filter out very short snippets
                text_parts.append(text)

    extracted_text = '\n\n'.join(text_parts)
    return _clean_text(extracted_text)


def _is_content_sufficient(text: str, min_length: int = 200) -> bool:
    """
    Check if extracted content is sufficient.
    JavaScript-heavy sites often return minimal text with simple scraping.
    """
    return len(text.strip()) >= min_length


def _scrape_with_requests(url: str, timeout: int = 10) -> str:
    """
    Scrape URL using simple HTTP request and BeautifulSoup.

    Args:
        url: URL to scrape
        timeout: Request timeout in seconds

    Returns:
        Extracted text content

    Raises:
        ScrapingError: If scraping fails
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')
        content = _extract_main_content(soup)

        return content

    except requests.exceptions.Timeout:
        raise ScrapingError(f"Request timed out after {timeout} seconds")
    except requests.exceptions.ConnectionError:
        raise ScrapingError("Unable to connect to the URL. Please check the URL and try again.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            raise ScrapingError("Access forbidden. The website may be blocking automated access.")
        elif e.response.status_code == 404:
            raise ScrapingError("Page not found. Please check the URL.")
        else:
            raise ScrapingError(f"HTTP error: {e.response.status_code}")
    except Exception as e:
        raise ScrapingError(f"Failed to scrape URL: {str(e)}")


def _scrape_with_playwright(url: str, timeout: int = 30000) -> str:
    """
    Scrape URL using Playwright for JavaScript-heavy sites.

    Args:
        url: URL to scrape
        timeout: Page load timeout in milliseconds

    Returns:
        Extracted text content

    Raises:
        ScrapingError: If scraping fails
    """
    try:
        with sync_playwright() as p:
            # Use Chromium browser
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()

            # Navigate to URL and wait for network to be idle
            page.goto(url, timeout=timeout, wait_until='networkidle')

            # Wait a bit for any dynamic content to load
            page.wait_for_timeout(2000)

            # Get the HTML content
            html_content = page.content()

            browser.close()

            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, 'lxml')
            content = _extract_main_content(soup)

            return content

    except PlaywrightTimeoutError:
        raise ScrapingError("Page load timed out. The website may be too slow or unresponsive.")
    except Exception as e:
        raise ScrapingError(f"Browser automation failed: {str(e)}")


def scrape_url(url: str) -> str:
    """
    Scrape job posting content from URL using hybrid approach.

    Tries simple HTTP request first, falls back to browser automation if content is insufficient.

    Args:
        url: URL of the job posting

    Returns:
        Extracted text content from the job posting

    Raises:
        ScrapingError: If scraping fails or returns insufficient content
    """
    # Validate URL format
    if not url.startswith(('http://', 'https://')):
        raise ScrapingError("Invalid URL format. URL must start with http:// or https://")

    # Try simple scraping first
    try:
        content = _scrape_with_requests(url)

        # Check if content is sufficient
        if _is_content_sufficient(content):
            return content

        # Content too short, might be JavaScript-heavy site
        # Fall back to browser automation
        print(f"Content insufficient ({len(content)} chars), trying browser automation...")

    except ScrapingError as e:
        # If simple scraping fails with access error, try browser automation
        if "forbidden" in str(e).lower() or "blocking" in str(e).lower():
            print(f"Simple scraping blocked, trying browser automation...")
        else:
            # For other errors, re-raise
            raise

    # Fall back to Playwright
    try:
        content = _scrape_with_playwright(url)

        if not _is_content_sufficient(content):
            raise ScrapingError(
                "Unable to extract sufficient content from the URL. "
                "The page may not contain a job posting or may have restricted access. "
                "Please try copying and pasting the job description text manually."
            )

        return content

    except ScrapingError:
        # Re-raise scraping errors as-is
        raise
    except Exception as e:
        raise ScrapingError(f"All scraping methods failed: {str(e)}")
