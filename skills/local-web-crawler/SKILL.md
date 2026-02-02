---
name: local-web-crawler
description: Local web crawler using Python (requests + BeautifulSoup). Crawls, searches, and extracts content from websites without external APIs. Requires venv with installed packages.
metadata: {"clawdbot":{"emoji":"🕸️","requires":{"bins":["python3"]},"setup":["cd /Users/mini-m4-1/clawd && source venv/bin/activate"]}}
---

# Local Web Crawler

Autonomous web crawler running locally without external APIs. Uses Python with requests and BeautifulSoup for scraping.

## Environment Setup

Activate the virtual environment before use:

```bash
source venv/bin/activate
```

The venv is pre-installed with:
- `requests` - HTTP client
- `beautifulsoup4` - HTML parser
- `lxml` - Fast XML/HTML parser

## Crawling a Website

### Basic Page Fetch

```bash
python3 scripts/fetch.py "https://example.com"
```

Output:
- Page title
- All links (absolute URLs)
- Text content (cleaned)
- Meta tags

### Search Within Page

```bash
python3 scripts/search.py "https://example.com" "search term"
```

Finds and highlights occurrences of the search term in the page.

### Extract Specific Elements

```bash
python3 scripts/extract.py "https://example.com" --tag "h1"
python3 scripts/extract.py "https://example.com" --tag "a" --limit 20
python3 scripts/extract.py "https://example.com" --class "article-content"
```

## Recursive Crawling

### Crawl to Depth

```bash
python3 scripts/crawl.py "https://example.com" --depth 2 --limit 50
```

- `--depth <n>`: How many levels deep to follow links (default: 1)
- `--limit <n>`: Max pages to visit (default: 100)
- `--output <file>`: Save results to JSON file

### Crawl With Filters

```bash
python3 scripts/crawl.py "https://example.com" \
  --include "/docs/*" \
  --exclude "/api/*" \
  --depth 3
```

- `--include`: Only crawl URLs matching pattern
- `--exclude`: Skip URLs matching pattern

## Content Extraction

### Extract Article Content

```bash
python3 scripts/article.py "https://example.com/article"
```

Automatically detects and extracts article content (title, body, author, date).

### Extract Product Data

```bash
python3 scripts/product.py "https://example.com/product/123"
```

Attempts to extract product information (name, price, description, images).

## Search & Index

### Build Local Index

```bash
python3 scripts/index.py "https://example.com" --depth 2
```

Builds a searchable index of the site content.

### Query Index

```bash
python3 scripts/query.py "search phrase"
```

Searches the built index for matching pages.

## Utilities

### Validate URLs

```bash
python3 scripts/validate.py "https://example.com/page1" "https://example.com/page2"
```

Check if URLs are accessible and return status codes.

### Download Images

```bash
python3 scripts/images.py "https://example.com/gallery" --output ./images
```

Downloads all images from a page to specified directory.

### Extract Emails

```bash
python3 scripts/emails.py "https://example.com/contact"
```

Finds all email addresses on a page.

## Advanced Usage

### Custom User-Agent

```bash
python3 scripts/fetch.py "https://example.com" --user-agent "Mozilla/5.0"
```

### Follow Redirects

```bash
python3 scripts/fetch.py "https://example.com" --follow-redirects
```

### Headers & Cookies

```bash
python3 scripts/fetch.py "https://example.com" \
  --header "Authorization: Bearer token" \
  --cookie "session=abc123"
```

### Rate Limiting

```bash
python3 scripts/crawl.py "https://example.com" --depth 3 --delay 2
```

Add delay between requests (seconds) to be polite.

## Output Formats

### JSON Output

```bash
python3 scripts/fetch.py "https://example.com" --json
```

Returns structured JSON instead of human-readable text.

### Markdown Output

```bash
python3 scripts/fetch.py "https://example.com" --markdown
```

Converts HTML content to clean Markdown.

## Integration with LM Studio

Use LM Studio embeddings to make searches semantic:

```bash
# Index with embeddings
python3 scripts/embed.py "https://example.com" --depth 2

# Semantic search
python3 scripts/semantic-search.py "conceptually similar phrase"
```

Requires LM Studio running at `http://localhost:1234/v1`

## Error Handling

The crawler automatically:
- Retries failed requests (3 attempts)
- Respects robots.txt
- Handles rate limits (429 responses)
- Skips malformed URLs
- Logs errors to `.logs/crawler.log`

## Best Practices

1. **Be polite**: Add delays between requests
2. **Respect robots.txt**: Crawler honors site rules
3. **Limit depth**: Deep crawling can be slow
4. **Cache results**: Use `--cache` flag to save/fetch from cache
5. **Filter URLs**: Use `--include`/`--exclude` for focused crawling

## Examples

### Research a Documentation Site

```bash
# Crawl docs and build index
python3 scripts/crawl.py "https://docs.example.com" \
  --include "/docs/*" \
  --depth 2 \
  --output docs-index.json

# Search for specific topics
python3 scripts/query.py "authentication API"
```

### Monitor a Blog

```bash
# Fetch latest posts
python3 scripts/crawl.py "https://blog.example.com" \
  --include "/post/*" \
  --depth 1 \
  --limit 10
```

### Extract Product Data

```bash
# Scrape product pages
python3 scripts/crawl.py "https://shop.example.com" \
  --include "/product/*" \
  --depth 1 \
  --output products.json

# Extract with product parser
python3 scripts/product.py "$(cat products.json | jq -r '.urls[0]')"
```

## Troubleshooting

### venv not activated
```
ModuleNotFoundError: No module named 'requests'
```
Solution: Run `source venv/bin/activate`

### Connection timeout
```
requests.exceptions.Timeout
```
Solution: Check internet connection, increase `--timeout` (default: 10s)

### 403 Forbidden
```
Status code: 403
```
Solution: Add custom User-Agent or headers

### Parsing errors
```
lxml.etree.XMLSyntaxError
```
Solution: Use `--parser html5lib` instead of lxml (install first)

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `fetch.py` | Fetch single page, extract content |
| `search.py` | Search text within page |
| `extract.py` | Extract specific HTML elements |
| `crawl.py` | Recursive site crawling |
| `index.py` | Build searchable index |
| `query.py` | Query built index |
| `article.py` | Extract article content |
| `product.py` | Extract product data |
| `validate.py` | Check URL accessibility |
| `images.py` | Download images |
| `emails.py` | Extract email addresses |
| `embed.py` | Index with embeddings |
| `semantic-search.py` | Semantic search via LM Studio |
