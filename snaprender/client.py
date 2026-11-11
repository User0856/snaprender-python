"""SnapRender API client."""

from __future__ import annotations

from typing import Any, Optional

import httpx


class SnapRenderError(Exception):
    """Error returned by the SnapRender API."""

    def __init__(self, message: str, code: str = "UNKNOWN", status: int = 0):
        super().__init__(message)
        self.code = code
        self.status = status


class SnapRender:
    """SnapRender Screenshot API client.

    Usage::

        snap = SnapRender(api_key="sk_live_...")
        image = snap.capture("https://example.com")
        with open("screenshot.png", "wb") as f:
            f.write(image)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://app.snap-render.com",
        timeout: float = 60.0,
    ):
        if not api_key:
            raise ValueError("api_key is required")
        self._base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self._base_url,
            headers={"X-API-Key": api_key},
            timeout=timeout,
        )

    def capture(
        self,
        url: Optional[str] = None,
        *,
        html: Optional[str] = None,
        markdown: Optional[str] = None,
        format: str = "png",
        width: Optional[int] = None,
        height: Optional[int] = None,
        full_page: Optional[bool] = None,
        lazy_load: Optional[bool] = None,
        quality: Optional[int] = None,
        delay: Optional[int] = None,
        dark_mode: Optional[bool] = None,
        block_ads: Optional[bool] = None,
        block_cookie_banners: Optional[bool] = None,
        hide_selectors: Optional[str] = None,
        click_selector: Optional[str] = None,
        device: Optional[str] = None,
        user_agent: Optional[str] = None,
        cache: Optional[bool] = None,
        cache_ttl: Optional[int] = None,
        response_type: Optional[str] = None,
    ) -> "bytes | dict[str, Any]":
        """Capture a screenshot. Provide exactly one of: url, html, or markdown.

        When html or markdown is provided, uses POST with JSON body.
        When url is provided, uses GET with query parameters (backward compatible).
        Returns bytes by default, or a dict when response_type='json'.
        """
        use_post = bool(html or markdown)

        if use_post:
            body: dict[str, Any] = {"format": format}
            if url is not None:
                body["url"] = url
            if html is not None:
                body["html"] = html
            if markdown is not None:
                body["markdown"] = markdown
            if width is not None:
                body["width"] = width
            if height is not None:
                body["height"] = height
            if full_page is not None:
                body["full_page"] = full_page
            if lazy_load is not None:
                body["lazy_load"] = lazy_load
            if quality is not None:
                body["quality"] = quality
            if delay is not None:
                body["delay"] = delay
            if dark_mode is not None:
                body["dark_mode"] = dark_mode
            if block_ads is not None:
                body["block_ads"] = block_ads
            if block_cookie_banners is not None:
                body["block_cookie_banners"] = block_cookie_banners
            if hide_selectors is not None:
                body["hide_selectors"] = hide_selectors
            if click_selector is not None:
                body["click_selector"] = click_selector
            if device is not None:
                body["device"] = device
            if user_agent is not None:
                body["user_agent"] = user_agent
            if cache is not None:
                body["cache"] = cache
            if cache_ttl is not None:
                body["cache_ttl"] = cache_ttl
            if response_type is not None:
                body["response_type"] = response_type

            resp = self._client.post("/v1/screenshot", json=body)
        else:
            if not url:
                raise ValueError("One of url, html, or markdown is required")
            params: dict[str, Any] = {"url": url, "format": format}
            if width is not None:
                params["width"] = width
            if height is not None:
                params["height"] = height
            if full_page is not None:
                params["full_page"] = str(full_page).lower()
            if lazy_load is not None:
                params["lazy_load"] = str(lazy_load).lower()
            if quality is not None:
                params["quality"] = quality
            if delay is not None:
                params["delay"] = delay
            if dark_mode is not None:
                params["dark_mode"] = str(dark_mode).lower()
            if block_ads is not None:
                params["block_ads"] = str(block_ads).lower()
            if block_cookie_banners is not None:
                params["block_cookie_banners"] = str(block_cookie_banners).lower()
            if hide_selectors is not None:
                params["hide_selectors"] = hide_selectors
            if click_selector is not None:
                params["click_selector"] = click_selector
            if device is not None:
                params["device"] = device
            if user_agent is not None:
                params["user_agent"] = user_agent
            if cache is not None:
                params["cache"] = str(cache).lower()
            if cache_ttl is not None:
                params["cache_ttl"] = cache_ttl
            if response_type is not None:
                params["response_type"] = response_type

            resp = self._client.get("/v1/screenshot", params=params)

        if resp.status_code != 200:
            self._raise_error(resp)
        if response_type == "json":
            return resp.json()
        return resp.content

    def sign(
        self,
        url: str,
        *,
        expires_in: Optional[int] = None,
        format: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        full_page: Optional[bool] = None,
        lazy_load: Optional[bool] = None,
        quality: Optional[int] = None,
        delay: Optional[int] = None,
        dark_mode: Optional[bool] = None,
        block_ads: Optional[bool] = None,
        block_cookie_banners: Optional[bool] = None,
        hide_selectors: Optional[str] = None,
        click_selector: Optional[str] = None,
        device: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> dict[str, Any]:
        """Generate a signed URL that can be used without an API key.

        Signing is free and does not count against your quota.
        The signed URL consumes one credit when rendered.
        Returns a dict with keys: signed_url, expires_at, expires_in.
        """
        body: dict[str, Any] = {"url": url}
        if expires_in is not None:
            body["expires_in"] = expires_in
        if format is not None:
            body["format"] = format
        if width is not None:
            body["width"] = width
        if height is not None:
            body["height"] = height
        if full_page is not None:
            body["full_page"] = full_page
        if lazy_load is not None:
            body["lazy_load"] = lazy_load
        if quality is not None:
            body["quality"] = quality
        if delay is not None:
            body["delay"] = delay
        if dark_mode is not None:
            body["dark_mode"] = dark_mode
        if block_ads is not None:
            body["block_ads"] = block_ads
        if block_cookie_banners is not None:
            body["block_cookie_banners"] = block_cookie_banners
        if hide_selectors is not None:
            body["hide_selectors"] = hide_selectors
        if click_selector is not None:
            body["click_selector"] = click_selector
        if device is not None:
            body["device"] = device
        if user_agent is not None:
            body["user_agent"] = user_agent

        resp = self._client.post("/v1/screenshot/sign", json=body)
        if resp.status_code != 200:
            self._raise_error(resp)
        return resp.json()

    def extract(
        self,
        url: str,
        *,
        type: str = "markdown",
        selector: Optional[str] = None,
        block_ads: Optional[bool] = None,
        block_cookie_banners: Optional[bool] = None,
        delay: Optional[int] = None,
        max_length: Optional[int] = None,
        cache: Optional[bool] = None,
        cache_ttl: Optional[int] = None,
    ) -> dict[str, Any]:
        """Extract content from a web page.

        Supports types: markdown, text, html, article, links, metadata.
        Returns a dict with keys: url, type, content, wordCount, processingTimeMs.
        """
        body: dict[str, Any] = {"url": url, "type": type}
        if selector is not None:
            body["selector"] = selector
        if block_ads is not None:
            body["block_ads"] = block_ads
        if block_cookie_banners is not None:
            body["block_cookie_banners"] = block_cookie_banners
        if delay is not None:
            body["delay"] = delay
        if max_length is not None:
            body["max_length"] = max_length
        if cache is not None:
            body["cache"] = cache
        if cache_ttl is not None:
            body["cache_ttl"] = cache_ttl

        resp = self._client.post("/v1/extract", json=body)
        if resp.status_code != 200:
            self._raise_error(resp)
        return resp.json()

    def batch(
        self,
        urls: list[str],
        *,
        format: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        full_page: Optional[bool] = None,
        lazy_load: Optional[bool] = None,
        quality: Optional[int] = None,
        delay: Optional[int] = None,
        dark_mode: Optional[bool] = None,
        block_ads: Optional[bool] = None,
        block_cookie_banners: Optional[bool] = None,
        hide_selectors: Optional[str] = None,
        click_selector: Optional[str] = None,
        device: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a batch screenshot job for multiple URLs (1-50).

        Returns immediately with a job ID. Poll with get_batch_status() for results.
        Each URL consumes one credit. Failed URLs get credits rolled back.
        """
        body: dict[str, Any] = {"urls": urls}
        if format is not None:
            body["format"] = format
        if width is not None:
            body["width"] = width
        if height is not None:
            body["height"] = height
        if full_page is not None:
            body["full_page"] = full_page
        if lazy_load is not None:
            body["lazy_load"] = lazy_load
        if quality is not None:
            body["quality"] = quality
        if delay is not None:
            body["delay"] = delay
        if dark_mode is not None:
            body["dark_mode"] = dark_mode
        if block_ads is not None:
            body["block_ads"] = block_ads
        if block_cookie_banners is not None:
            body["block_cookie_banners"] = block_cookie_banners
        if hide_selectors is not None:
            body["hide_selectors"] = hide_selectors
        if click_selector is not None:
            body["click_selector"] = click_selector
        if device is not None:
            body["device"] = device
        if user_agent is not None:
            body["user_agent"] = user_agent

        resp = self._client.post("/v1/screenshot/batch", json=body)
        if resp.status_code not in (200, 202):
            self._raise_error(resp)
        return resp.json()

    def get_batch_status(self, job_id: str) -> dict[str, Any]:
        """Get the status of a batch screenshot job.

        Poll this until status is 'completed' or 'failed'.
        """
        resp = self._client.get(f"/v1/screenshot/batch/{job_id}")
        if resp.status_code != 200:
            self._raise_error(resp)
        return resp.json()

    def create_webhook(
        self,
        url: str,
        events: list[str],
    ) -> dict[str, Any]:
        """Create a webhook for event notifications.

        Max 5 webhooks per account.
        Events: screenshot.completed, quota.warning, quota.exceeded.
        Returns the webhook with its signing secret.
        """
        body: dict[str, Any] = {"url": url, "events": events}
        resp = self._client.post("/v1/webhooks", json=body)
        if resp.status_code not in (200, 201):
            self._raise_error(resp)
        return resp.json()

    def list_webhooks(self) -> list[dict[str, Any]]:
        """List all webhooks for the authenticated account."""
        resp = self._client.get("/v1/webhooks")
        if resp.status_code != 200:
            self._raise_error(resp)
        return resp.json()

    def delete_webhook(self, webhook_id: str) -> None:
        """Delete a webhook by ID."""
        resp = self._client.delete(f"/v1/webhooks/{webhook_id}")
        if resp.status_code not in (200, 204):
            self._raise_error(resp)

    def test_webhook(self, webhook_id: str) -> dict[str, Any]:
        """Send a test payload to a webhook."""
        resp = self._client.post(f"/v1/webhooks/{webhook_id}/test")
        if resp.status_code != 200:
            self._raise_error(resp)
        return resp.json()

    @staticmethod
    def verify_webhook_signature(payload: str, signature: str, secret: str) -> bool:
        """Verify a webhook signature.

        Use in your webhook handler to confirm the payload was sent by SnapRender.
        """
        import hmac
        import hashlib
        expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        sig = signature.removeprefix("sha256=")
        return hmac.compare_digest(sig, expected)

    def info(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """Get cache info for a URL without capturing.

        Returns a dict with keys: url, cached, cache_key, cached_at,
        expires_at, content_type.
        """
        params: dict[str, Any] = {"url": url, **kwargs}
        resp = self._client.get("/v1/screenshot/info", params=params)
        if resp.status_code != 200:
            self._raise_error(resp)
        data = resp.json()
        return {
            "url": data["url"],
            "cached": data["cached"],
            "cache_key": data.get("cache_key"),
            "cached_at": data.get("cached_at"),
            "expires_at": data.get("expires_at"),
            "content_type": data.get("content_type"),
        }

    def usage(self) -> dict[str, Any]:
        """Get current month's usage.

        Returns a dict with keys: plan, used, limit, remaining, period.
        """
        resp = self._client.get("/v1/usage")
        if resp.status_code != 200:
            self._raise_error(resp)
        data = resp.json()
        return {
            "plan": data["plan"],
            "used": data["usage"]["screenshots_used"],
            "limit": data["usage"]["screenshots_limit"],
            "remaining": data["usage"]["screenshots_remaining"],
            "period": data["period"],
        }

    def usage_daily(self, days: int = 30) -> dict[str, Any]:
        """Get daily usage breakdown."""
        resp = self._client.get("/v1/usage/daily", params={"days": days})
        if resp.status_code != 200:
            self._raise_error(resp)
        return resp.json()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> SnapRender:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    @staticmethod
    def _raise_error(resp: httpx.Response) -> None:
        try:
            body = resp.json()
            err = body.get("error", {})
            raise SnapRenderError(
                err.get("message", f"HTTP {resp.status_code}"),
                err.get("code", "UNKNOWN"),
                resp.status_code,
            )
        except (ValueError, KeyError):
            raise SnapRenderError(f"HTTP {resp.status_code}", "UNKNOWN", resp.status_code)
