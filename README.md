<a href="https://snap-render.com"><img src="https://snap-render.com/brand/snaprender-icon-128.png" alt="SnapRender" width="64" height="64"></a>

# snaprender

[![PyPI version](https://img.shields.io/pypi/v/snaprender)](https://pypi.org/project/snaprender/)
[![PyPI downloads](https://img.shields.io/pypi/dm/snaprender)](https://pypi.org/project/snaprender/)
[![license](https://img.shields.io/pypi/l/snaprender)](https://pypi.org/project/snaprender/)

Official Python SDK for the [SnapRender](https://snap-render.com) Screenshot API. Capture pixel-perfect screenshots, extract page content, run batch jobs, and manage webhooks with a single library.

**200 free screenshots/month. [Get your API key](https://snap-render.com/auth/signup?ref=pypi)**

## Features

- **Multiple output formats** : PNG, JPEG, WebP, and PDF
- **Three input modes** : URL, raw HTML, or Markdown
- **Signed URLs** : generate pre-signed screenshot URLs (no API key needed at render time)
- **Content extraction** : pull Markdown, plain text, HTML, article, links, or metadata from any page
- **Batch screenshots** : capture up to 50 URLs in a single job
- **Webhooks** : receive real-time notifications for screenshot and quota events
- **Device emulation** : iPhone, iPad, Pixel, and more presets
- **Dark mode** : capture pages with `prefers-color-scheme: dark`
- **Ad blocking** : remove ads automatically before capture
- **Cookie banner removal** : clean screenshots without consent popups
- **Smart caching** : configurable CDN cache with TTL control
- **Full-page captures** : screenshot the entire scrollable page

## Install

```bash
pip install snaprender
```

## Quick Start

```python
from snaprender import SnapRender

snap = SnapRender(api_key="sk_live_...")

# Capture by URL
image = snap.capture("https://example.com")
with open("screenshot.png", "wb") as f:
    f.write(image)

# Capture from raw HTML
image = snap.capture(html="<h1>Hello World</h1>")

# Capture from Markdown
image = snap.capture(markdown="# Hello World\nSome **bold** text.")
```

> **Cache is OFF by default.** Every request captures a fresh screenshot. To save credits on repeated requests, pass `cache=True`. Cached hits are free and return in under 200ms:
>
> ```python
> image = snap.capture("https://example.com", cache=True)
> ```

## Context Manager

```python
with SnapRender(api_key="sk_live_...") as snap:
    image = snap.capture("https://example.com")
```

The HTTP connection is closed automatically when the block exits.

## API Reference

### Constructor

```python
SnapRender(api_key, base_url="https://app.snap-render.com", timeout=60.0)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | (required) | Your SnapRender API key (`sk_live_...`) |
| `base_url` | str | `"https://app.snap-render.com"` | API base URL |
| `timeout` | float | `60.0` | Request timeout in seconds |

---

### `snap.capture(url, *, html, markdown, **options)` -> `bytes | dict`

Take a screenshot. Provide exactly **one** of `url`, `html`, or `markdown`.

- When `url` is provided alone, the request is sent as GET with query parameters.
- When `html` or `markdown` is provided, the request is sent as POST with a JSON body.
- Returns raw image bytes by default. Set `response_type="json"` to get a dict with metadata and a base64 data URI.

```python
# URL with options
jpg = snap.capture(
    "https://example.com",
    format="jpeg",
    width=1920,
    height=1080,
    full_page=True,
    dark_mode=True,
    quality=95,
)

# HTML input
png = snap.capture(html="<h1 style='color:red'>Red Title</h1>", width=800)

# Markdown input
png = snap.capture(markdown="# Report\n\n| Col A | Col B |\n|-------|-------|\n| 1 | 2 |")

# JSON response (base64 data URI + metadata)
result = snap.capture("https://example.com", response_type="json")
print(result["image"])  # data:image/png;base64,...
```

**Options**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `url` | str | `None` | URL to capture |
| `html` | str | `None` | Raw HTML to render |
| `markdown` | str | `None` | Markdown to render |
| `format` | str | `"png"` | `"png"`, `"jpeg"`, `"webp"`, or `"pdf"` |
| `width` | int | `1280` | Viewport width in pixels |
| `height` | int | `800` | Viewport height in pixels |
| `full_page` | bool | `False` | Capture the full scrollable page |
| `lazy_load` | bool | `False` | With `full_page`, scroll through the page first so lazy-loaded images appear (usually 1-5 s slower). Ignored unless `full_page` is true |
| `quality` | int | `90` | JPEG/WebP quality (1-100) |
| `delay` | int | `0` | Wait (ms) after page load before capture |
| `dark_mode` | bool | `False` | Emulate dark color scheme |
| `block_ads` | bool | `True` | Block ad networks |
| `block_cookie_banners` | bool | `True` | Remove cookie consent banners |
| `device` | str | `None` | Device preset: `"iphone_14"`, `"iphone_15_pro"`, `"pixel_7"`, `"ipad_pro"`, `"macbook_pro"` |
| `hide_selectors` | str | `None` | Comma-separated CSS selectors to hide |
| `click_selector` | str | `None` | CSS selector to click before capture |
| `user_agent` | str | `None` | Custom user-agent string |
| `cache` | bool | `False` | Return cached result if available. **Off by default:** set `True` to enable caching. Cached hits are free but may be up to 24h old. |
| `cache_ttl` | int | `86400` | Cache lifetime in seconds (default 24h). Cached screenshots older than this are recaptured. |
| `response_type` | str | `None` | Set to `"json"` for metadata + base64 data URI |

---

### `snap.sign(url, *, expires_in, **options)` -> `dict`

Generate a signed URL that can be used without an API key. Signing itself is free and does not count against your quota. One credit is consumed when the signed URL is rendered.

```python
result = snap.sign(
    "https://example.com",
    expires_in=3600,       # optional, seconds until expiry
    format="png",
    width=1280,
    dark_mode=True,
)
print(result["signed_url"])   # use this in <img> tags, emails, etc.
print(result["expires_at"])   # ISO 8601 timestamp
```

**Options**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `url` | str | (required) | URL to capture |
| `expires_in` | int | `None` | Seconds until the signed URL expires |
| `format` | str | `None` | `"png"`, `"jpeg"`, `"webp"`, or `"pdf"` |
| `width` | int | `None` | Viewport width |
| `height` | int | `None` | Viewport height |
| `full_page` | bool | `None` | Full-page capture |
| `lazy_load` | bool | `None` | With `full_page`, load lazy images first |
| `quality` | int | `None` | JPEG/WebP quality |
| `delay` | int | `None` | Wait (ms) after load |
| `dark_mode` | bool | `None` | Emulate dark mode |
| `block_ads` | bool | `None` | Block ads |
| `block_cookie_banners` | bool | `None` | Remove cookie banners |
| `hide_selectors` | str | `None` | CSS selectors to hide |
| `click_selector` | str | `None` | CSS selector to click |
| `device` | str | `None` | Device preset |
| `user_agent` | str | `None` | Custom user-agent |

**Returns** `{ "signed_url": str, "expires_at": str, "expires_in": int }`

---

### `snap.extract(url, *, type, **options)` -> `dict`

Extract content from a web page. Six extraction types are available:

| Type | Description |
|------|-------------|
| `"markdown"` | Page content converted to Markdown (default) |
| `"text"` | Plain text, all tags stripped |
| `"html"` | Cleaned HTML |
| `"article"` | Article body extracted via Readability |
| `"links"` | All links on the page |
| `"metadata"` | Title, description, Open Graph tags, etc. |

```python
# Extract as Markdown
result = snap.extract("https://example.com", type="markdown")
print(result["content"])
print(result["wordCount"])

# Extract just the article body
article = snap.extract("https://example.com/blog/post", type="article")

# Extract metadata
meta = snap.extract("https://example.com", type="metadata")

# Scope extraction to a specific element
result = snap.extract(
    "https://example.com",
    type="text",
    selector="#main-content",
    max_length=5000,
)
```

**Options**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `url` | str | (required) | URL to extract from |
| `type` | str | `"markdown"` | Extraction type (see table above) |
| `selector` | str | `None` | CSS selector to scope extraction |
| `block_ads` | bool | `None` | Block ads before extraction |
| `block_cookie_banners` | bool | `None` | Remove cookie banners |
| `delay` | int | `None` | Wait (ms) after page load |
| `max_length` | int | `None` | Truncate content to this many characters |
| `cache` | bool | `None` | Return cached extraction if available. **Off by default:** set `True` to enable caching. Cached hits are free but may be stale. |
| `cache_ttl` | int | `None` | Cache lifetime in seconds (default 24h). |

**Returns** `{ "url": str, "type": str, "content": ..., "wordCount": int, "processingTimeMs": int }`

---

### `snap.batch(urls, **options)` -> `dict`

Create a batch screenshot job for 1 to 50 URLs. The call returns immediately with a job ID. Each URL consumes one credit; credits for failed URLs are rolled back.

```python
job = snap.batch(
    ["https://example.com", "https://example.org", "https://example.net"],
    format="png",
    width=1280,
    dark_mode=True,
)
print(job["jobId"])  # use this to poll status
```

**Options**: same screenshot options as `capture()` (except `url`, `html`, `markdown`, `response_type`, `cache`, `cache_ttl`). These options apply to every URL in the batch.

**Returns** `{ "jobId": str, "status": str, "statusUrl": str, "total": int, "completed": int, "failed": int, "items": list, ... }`

---

### `snap.get_batch_status(job_id)` -> `dict`

Poll the status of a batch job. Keep polling until `status` is `"completed"` or `"failed"`.

```python
import time

job = snap.batch(["https://example.com", "https://example.org"])

while True:
    status = snap.get_batch_status(job["jobId"])
    print(f"{status['status']} - {status.get('completed', 0)}/{status['total']}")
    if status["status"] in ("completed", "failed"):
        break
    time.sleep(2)

# Download results
for item in status["items"]:
    if item["status"] == "completed":
        print(item["url"], item["downloadUrl"])
    else:
        print(item["url"], item.get("error"))
```

---

### `snap.create_webhook(url, events)` -> `dict`

Register a webhook endpoint to receive event notifications. Maximum 5 webhooks per account.

Available events: `screenshot.completed`, `quota.warning`, `quota.exceeded`

```python
webhook = snap.create_webhook(
    url="https://yoursite.com/webhooks/snaprender",
    events=["screenshot.completed", "quota.warning"],
)
print(webhook["id"])
print(webhook["secret"])  # save this for signature verification
```

---

### `snap.list_webhooks()` -> `list[dict]`

List all webhooks registered on your account.

```python
webhooks = snap.list_webhooks()
for wh in webhooks:
    print(wh["id"], wh["url"], wh["events"])
```

---

### `snap.delete_webhook(webhook_id)` -> `None`

Delete a webhook by its ID.

```python
snap.delete_webhook("wh_abc123")
```

---

### `snap.test_webhook(webhook_id)` -> `dict`

Send a test payload to a webhook endpoint. Useful for verifying your handler works before relying on real events.

```python
result = snap.test_webhook("wh_abc123")
print(result)  # delivery status
```

---

### `SnapRender.verify_webhook_signature(payload, signature, secret)` -> `bool`

Static method. Verify the HMAC-SHA256 signature of an incoming webhook payload. Use this in your webhook handler to confirm the request was sent by SnapRender.

```python
from snaprender import SnapRender

# In your webhook handler (e.g., Flask)
@app.route("/webhooks/snaprender", methods=["POST"])
def handle_webhook():
    payload = request.get_data(as_text=True)
    signature = request.headers.get("X-Signature")
    secret = "whsec_..."  # from create_webhook response

    if not SnapRender.verify_webhook_signature(payload, signature, secret):
        return "Invalid signature", 403

    event = request.get_json()
    print(event["type"], event["data"])
    return "OK", 200
```

---

### `snap.info(url)` -> `dict`

Check if a screenshot is cached for a given URL, without capturing it. No credits are consumed.

```python
info = snap.info("https://example.com")
print(info["cached"])      # True or False
print(info["expires_at"])  # ISO timestamp (when cached)
```

**Returns** `{ "url": str, "cached": bool, "cache_key": str | None, "cached_at": str | None, "expires_at": str | None, "content_type": str | None }`

---

### `snap.usage()` -> `dict`

Get the current billing period's usage summary.

```python
usage = snap.usage()
print(f"{usage['used']}/{usage['limit']} screenshots used")
print(f"Plan: {usage['plan']}, Remaining: {usage['remaining']}")
```

**Returns** `{ "plan": str, "used": int, "limit": int, "remaining": int, "period": dict }`

---

### `snap.usage_daily(days=30)` -> `dict`

Get a day-by-day usage breakdown.

```python
daily = snap.usage_daily(days=7)
for day in daily["daily"]:
    print(day["date"], day["count"])
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `days` | int | `30` | Number of days to include |

---

## LangChain Integration

Use SnapRender as a [LangChain](https://python.langchain.com/) tool for AI agents:

```python
import os
from langchain_core.tools import tool
from snaprender import SnapRender

client = SnapRender(api_key=os.environ["SNAPRENDER_API_KEY"])

@tool
def take_screenshot(url: str, format: str = "png", dark_mode: bool = False) -> str:
    """Capture a screenshot of any website URL. Returns base64 data URI."""
    result = client.capture(
        url, format=format, dark_mode=dark_mode, response_type="json"
    )
    return result["image"]
```

Works with LangGraph, CrewAI, and any framework that supports LangChain tools.

## Error Handling

All API errors raise `SnapRenderError` with `code`, `status`, and a human-readable message.

```python
from snaprender import SnapRender, SnapRenderError

snap = SnapRender(api_key="sk_live_...")

try:
    snap.capture("https://example.com")
except SnapRenderError as e:
    print(e.code)    # "QUOTA_EXCEEDED"
    print(e.status)  # 429
    print(e)         # "Monthly quota exceeded"
```

Common error codes: `INVALID_API_KEY`, `QUOTA_EXCEEDED`, `INVALID_URL`, `VALIDATION_ERROR`, `SCREENSHOT_FAILED`.

## Links

- [Documentation](https://snap-render.com/docs)
- [Pricing](https://snap-render.com/pricing)
- [Dashboard](https://app.snap-render.com/dashboard)
- [Blog](https://snap-render.com/blog)

## License

MIT
